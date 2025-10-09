# 代码生成时间: 2025-10-09 16:51:45
import logging
import json
from celery import Celery
from celery.utils.log import get_task_logger

# 设置 Celery 配置
app = Celery('form_data_validator', broker='redis://localhost:6379/0')
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone="UTC",
    enable_utc=True,
)

logger = get_task_logger(__name__)


# 定义表单数据验证器任务
@app.task(name='validate_form_data', bind=True)
def validate_form_data(self, form_data):
    """
    验证表单数据的 Celery 任务
    
    参数:
    form_data (dict): 表单数据，必须包含 'username' 和 'email' 字段
    
    返回:
    dict: 包含 'is_valid' 和 'errors' 的字典
    
    异常:
    ValueError: 如果表单数据不包含必要的字段
    """
    try:
        # 检查表单数据是否包含必要的字段
        required_fields = ['username', 'email']
        for field in required_fields:
            if field not in form_data:
                raise ValueError(f'field {field} is missing in the form data')

        # 验证用户名
        if not form_data['username'] or len(form_data['username']) < 3:
            return {'is_valid': False, 'errors': [f'Username must be at least 3 characters long']}

        # 验证电子邮件地址
        if '@' not in form_data['email']:
            return {'is_valid': False, 'errors': ['Invalid email address']}

        # 如果所有验证通过
        return {'is_valid': True, 'errors': []}

    except Exception as e:
        # 记录异常信息
        logger.error('Error validating form data', exc_info=True)
        raise self.retry(exc=e)


if __name__ == '__main__':
    # 配置日志
    logging.basicConfig(level=logging.INFO)
    logger.setLevel(logging.INFO)
    
    # 示例表单数据
    sample_form_data = {
        'username': 'john_doe',
        'email': 'john@example.com',
    }
    
    # 调用任务验证表单数据
    result = validate_form_data.delay(sample_form_data)
    
    # 获取结果
    validated_data = result.get()
    print(json.dumps(validated_data, indent=4))
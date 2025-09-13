# 代码生成时间: 2025-09-13 09:58:45
import os
import random
from celery import Celery

# 设置Celery
app = Celery('random_number_generator', broker=os.environ['CELERY_BROKER_URL'])

@app.task(bind=True)
def generate_random_number(self, min_value, max_value):
    '''
    生成指定范围的随机数
    :param self: Celery任务实例
    :param min_value: 随机数最小值
    :param max_value: 随机数最大值
    :return: 随机数
    '''
    # 检查输入值是否有效
    if min_value >= max_value:
        raise ValueError('最小值必须小于最大值')

    # 生成随机数
    random_number = random.randint(min_value, max_value)
    return random_number

# 错误处理示例
if __name__ == '__main__':
    try:
        # 调用随机数生成器
        result = generate_random_number.delay(1, 100)
        print('随机数:', result.get(timeout=10))
    except ValueError as e:
        print('错误:', e)
    except Exception as e:
        print('发生未知错误:', e)
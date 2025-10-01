# 代码生成时间: 2025-10-02 03:53:22
import hashlib
import base64
from celery import Celery
from celery.utils.log import get_task_logger

# 获取Celery的日志记录器
logger = get_task_logger(__name__)

# 配置Celery应用
app = Celery('digital_signature_tool',
             broker='pyamqp://guest@localhost//',
             backend='rpc://')

@app.task(name='generate_signature', bind=True)
def generate_signature(self, data):
    """
    生成数字签名

    :param self: Celery任务实例
    :param data: 待签名的原始数据，字符串类型
    :return: 签名结果的Base64编码字符串
    """
    try:
        # 使用SHA256算法对数据进行哈希处理
        hash_object = hashlib.sha256(data.encode('utf-8'))
        # 获取哈希值的十六进制表示
        signature = hash_object.hexdigest()
        # 返回签名结果的Base64编码
        return base64.b64encode(signature.encode('utf-8')).decode('utf-8')
    except Exception as e:
        # 记录异常信息
        logger.error(f'Error generating signature: {e}')
        raise

if __name__ == '__main__':
    # 测试生成签名
    data = 'Hello, World!'
    signature = generate_signature.delay(data).get()
    print(f'Signature for "{data}": {signature}')
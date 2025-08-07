# 代码生成时间: 2025-08-07 14:15:50
import os
import socket
from celery import Celery
from celery.utils.log import get_task_logger

# 设置Celery配置
app = Celery('network_connection_checker', broker='pyamqp://guest@localhost//')
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_backend='rpc://',
    timezone='UTC',
    enable_utc=True,
)

# 获取Celery任务日志记录器
logger = get_task_logger(__name__)

def check_connection(host, port):
    """检查指定主机和端口的网络连接状态"""
    try:
        # 尝试建立TCP连接
        sock = socket.create_connection((host, port), timeout=5)
        sock.close()
        return True
    except socket.error as e:
        # 记录和处理连接错误
        logger.error(f'Connection error: {e}')
        return False

@app.task(name='check_connection_task')
def check_connection_task(host, port):
    """异步检查网络连接状态的任务"""
    try:
        # 调用连接检查函数
        connection_status = check_connection(host, port)
        return {'status': 'success', 'result': connection_status}
    except Exception as e:
        # 处理任何未预见的错误
        logger.error(f'An error occurred: {e}')
        return {'status': 'error', 'message': str(e)}

# 如果这是主程序，则运行测试代码
if __name__ == '__main__':
    # 测试代码，检查特定主机和端口的连接状态
    result = check_connection_task.apply(args=['www.google.com', 80])
    print(result.get())

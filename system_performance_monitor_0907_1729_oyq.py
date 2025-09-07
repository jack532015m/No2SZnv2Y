# 代码生成时间: 2025-09-07 17:29:51
import os
import psutil
from celery import Celery

# 定义Celery应用
app = Celery('system_performance_monitor',
             broker='amqp://guest@localhost//')

# 任务装饰器，用于异步执行监控任务
@app.task(bind=True)
def monitor_performance(self):
    """监控系统性能，并返回监控结果。"""
    try:
        # 获取CPU使用率
        cpu_usage = psutil.cpu_percent(interval=1)

        # 获取内存使用情况
        memory_usage = psutil.virtual_memory().percent

        # 获取磁盘使用情况
        disk_usage = psutil.disk_usage('/').percent

        # 打印监控结果
        print(f'CPU Usage: {cpu_usage}%')
        print(f'Memory Usage: {memory_usage}%')
        print(f'Disk Usage: {disk_usage}%')

        # 将监控结果返回
        return {'cpu_usage': cpu_usage,
                'memory_usage': memory_usage,
                'disk_usage': disk_usage}
    except Exception as e:
        # 错误处理
        print(f'Error monitoring performance: {e}')
        self.retry(exc=e)  # 重试失败的任务


def main():
    """主函数，用于初始化Celery应用和启动监控任务。"""
    # 启动Celery worker
    app.start()

    # 启动监控任务
    monitor_performance.apply_async()

if __name__ == '__main__':
    main()

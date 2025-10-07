# 代码生成时间: 2025-10-08 03:10:22
import os
import logging
from celery import Celery
from celery.exceptions import SoftTimeLimitExceeded

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 定义 Celery 实例
app = Celery('report_generator',
             broker='pyamqp://guest@localhost//',
             backend='rpc://')

# 模拟报表生成函数
def generate_report(data):
    """
    生成报表的模拟函数
    :param data: 报表数据
    :return: 生成的报表文件路径
    """
    try:
        # 模拟长时间运行的任务
        from time import sleep
        sleep(10)  # 模拟耗时操作
        report_path = 'report.pdf'
        # 假设这里是生成报表的代码
        # 这里我们只是简单地创建一个文件作为示例
        with open(report_path, 'w') as f:
            f.write('Generated Report')
        return report_path
    except Exception as e:
        logger.error(f'Failed to generate report: {e}')
        raise

# Celery 任务
@app.task(soft_time_limit=30)
def create_report_task(data):
    """
    使用 Celery 执行报表生成任务
    :param data: 报表数据
    :return: 报表文件路径
    """
    try:
        # 使用 Celery 任务执行报表生成
        report_path = generate_report(data)
        logger.info(f'Report generated successfully at {report_path}')
        return report_path
    except SoftTimeLimitExceeded as e:
        logger.error('Report generation exceeded the time limit')
        raise
    except Exception as e:
        logger.error(f'Error in report generation: {e}')
        raise

if __name__ == '__main__':
    # 测试 Celery 任务
    try:
        report_path = create_report_task.delay({'data': 'sample_data'})
        report_path.wait()  # 等待任务完成
        logger.info(f'Report generated at: {report_path.get() if report_path.ready() else "Task still running"}')
    except Exception as e:
        logger.error(f'Failed to run report generation task: {e}')
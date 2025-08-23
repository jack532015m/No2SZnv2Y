# 代码生成时间: 2025-08-23 11:28:48
import os
from celery import Celery
from celery import shared_task
import pandas as pd
from openpyxl import Workbook
from openpyxl import load_workbook

# 定义Celery应用
app = Celery('excel_generator', broker='pyamqp://guest@localhost//')

# 定义一个函数来生成Excel文件
@shared_task(bind=True,
             soft_time_limit=60,
             time_limit=120,
             max_retries=3,
             default_retry_delay=60)
def generate_excel_file(self, file_name, data):
    """
    Generate an Excel file with the given data.

    :param self: The Celery task instance.
    :param file_name: The name of the Excel file to generate.
    :param data: A dictionary containing the data to populate the Excel file.
    :return: None
    """
    try:
        # 确保文件名是安全的
        if not file_name.endswith('.xlsx'):
            raise ValueError("File name must end with '.xlsx'")

        # 使用Pandas来创建DataFrame
        df = pd.DataFrame(data)

        # 将DataFrame保存为Excel文件
        df.to_excel(file_name, index=False)

        # 记录成功生成Excel文件的日志
        self.retry(exc=None)  # 停止重试
    except Exception as e:
        # 如果有异常发生，则重新抛出异常，以便Celery可以进行重试
        raise self.retry(exc=e)

    # 返回文件路径
    return os.path.abspath(file_name)

# 以下是一个示例函数，用于演示如何调用generate_excel_file函数
def example_usage():
    # 示例数据，格式为字典列表
    data = {
        'Name': ['John', 'Jane', 'Alice'],
        'Age': [28, 22, 35],
        'City': ['New York', 'Los Angeles', 'Chicago']
    }

    # 调用Celery任务来生成Excel文件
    file_path = generate_excel_file.delay('example.xlsx', data)
    print(f'Excel file generated at: {file_path}')

if __name__ == '__main__':
    example_usage()

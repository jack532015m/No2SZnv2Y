# 代码生成时间: 2025-09-14 18:05:36
import os
from celery import Celery
from openpyxl import Workbook

# 配置Celery
app = Celery('excel_generator', broker='pyamqp://guest@localhost//')

@app.task
def generate_excel(data, file_path):
    """
    生成一个Excel文件
    :param data: 要写入Excel的数据，格式为二维列表
    :param file_path: Excel文件保存的路径
    :return: 无
    """
    try:
        # 创建一个Workbook
        wb = Workbook()
        # 选择默认的Active Worksheet
        ws = wb.active

        # 写入数据到Excel
        for row_data in data:
            ws.append(row_data)

        # 保存到指定路径
        wb.save(file_path)
        print(f"Excel文件已成功生成: {file_path}")
    except Exception as e:
        # 错误处理
        print(f"生成Excel文件时发生错误: {e}")

if __name__ == '__main__':
    # 演示：生成一个包含数据的Excel文件
    data = [
        ['姓名', '年龄', '城市'],
        ['Alice', 28, 'New York'],
        ['Bob', 22, 'Los Angeles'],
        ['Charlie', 35, 'Chicago']
    ]
    file_path = 'example.xlsx'
    # 调用任务生成Excel文件
    generate_excel.delay(data, file_path)
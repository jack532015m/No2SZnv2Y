# 代码生成时间: 2025-09-21 23:11:22
import os
from celery import Celery

# 定义配置文件路径
CONFIG_FILE_PATH = 'config.json'

# 初始化Celery应用
app = Celery('config_manager',
             broker='pyamqp://guest@localhost//')
app.conf.update(
    result_backend='rpc://',
    task_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
)

# 读取配置文件
def read_config_file(file_path):
    """读取配置文件内容"""
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"配置文件 {file_path} 不存在")
    except Exception as e:
        raise Exception(f"读取配置文件时发生错误: {e}")

# 写入配置文件
def write_config_file(file_path, config_data):
    """将配置数据写入文件"""
    try:
        with open(file_path, 'w') as file:
            file.write(config_data)
    except Exception as e:
        raise Exception(f"写入配置文件时发生错误: {e}")

# Celery任务：读取配置
@app.task
def read_config():
    """Celery任务：读取配置文件"""
    try:
        config_data = read_config_file(CONFIG_FILE_PATH)
        return config_data
    except Exception as e:
        return f"Error: {e}"

# Celery任务：写入配置
@app.task
def write_config(config_data):
    """Celery任务：写入配置到文件"""
    try:
        write_config_file(CONFIG_FILE_PATH, config_data)
        return "配置写入成功"
    except Exception as e:
        return f"Error: {e}"

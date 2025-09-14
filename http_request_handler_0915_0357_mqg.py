# 代码生成时间: 2025-09-15 03:57:01
import os
import requests
from celery import Celery
from flask import Flask, request, jsonify

# 配置Flask应用
app = Flask(__name__)

# 配置Celery应用
broker_url = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
result_backend = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
c = Celery('tasks', broker=broker_url, backend=result_backend)
c.conf.update(app.config)

# 定义Celery任务
@c.task()
def process_http_request(url, method, data=None):
    """处理HTTP请求的任务."""
    try:
        if method.upper() == 'GET':
            response = requests.get(url)
        elif method.upper() == 'POST':
            response = requests.post(url, json=data)
        else:
            raise ValueError('Unsupported HTTP method')
        return {'status_code': response.status_code, 'response': response.text}
    except Exception as e:
        return {'error': str(e)}

# 定义Flask路由
@app.route('/send_request', methods=['POST'])
def send_request():
    "
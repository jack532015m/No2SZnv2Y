# 代码生成时间: 2025-08-01 17:40:57
import os
import sys
from celery import Celery
from celery.exceptions import Reject
import requests
from requests.exceptions import RequestException
from flask import Flask, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash

# 配置Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
app = Celery('tasks', broker='pyamqp://guest@localhost//')
app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
)

# Flask应用
app_flask = Flask(__name__)

# 用户认证数据库（示例）
users_db = {
    "user1": generate_password_hash("password1"),
    "user2": generate_password_hash("password2"),
}

# 用户认证任务
@app.task
def authenticate_user(username, password):
    """
    用户认证任务
    :param username: 用户名
    :param password: 密码
    :return: 认证结果
    """
    try:
        # 检查用户名和密码
        if username not in users_db:
            raise Exception("Username not found.")
        if not check_password_hash(users_db[username], password):
            raise Exception("Password is incorrect.")
        return {"status": "success", "message": "Authentication successful."}
    except Exception as e:
        # 处理认证错误
        raise Reject(str(e), exc=e)

# Flask路由 - 用户认证接口
@app_flask.route('/auth', methods=['POST'])
def auth():
    """
    用户认证接口
    """
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return jsonify({'status': 'error', 'message': 'Username or password is required.'}), 400

        # 调用Celery任务进行认证
        result = authenticate_user.delay(username, password)
        return jsonify({'status': 'success', 'message': 'Authentication task started.'}), 202
    except RequestException as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    # 运行Flask应用
    app_flask.run(debug=True)

# 代码生成时间: 2025-08-06 19:47:59
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from celery import Celery

# Flask application setup
app = Flask(__name__)
CORS(app)

# Celery setup
def make_celery(app):
    """
    Initialize Celery with the Flask application context.
    """
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    return celery

celery = make_celery(app)

# Celery task example
@celery.task(name='example_task')
def example_task(arg1, arg2):
    """
    An example Celery task that can be called asynchronously.
    """
    # Simulate some asynchronous processing
    return arg1 + arg2

# API endpoints
@app.route('/api/sum', methods=['POST'])
def sum_api():
    """
    API endpoint to calculate the sum of two numbers.
    """
    try:
        data = request.get_json()
        if not data or 'num1' not in data or 'num2' not in data:
            return jsonify({'error': 'Missing parameters'}), 400

        num1 = data['num1']
        num2 = data['num2']

        # Call the Celery task asynchronously
        result = example_task.delay(num1, num2)
        return jsonify({'message': 'Task started', 'task_id': result.id}), 202
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Ensure the broker URL and result backend are set in the environment variables
    if not all([key in os.environ for key in ['CELERY_BROKER_URL', 'CELERY_RESULT_BACKEND']]):
        raise RuntimeError('CELERY_BROKER_URL and CELERY_RESULT_BACKEND must be set in the environment')

    app.run(debug=True)

# 代码生成时间: 2025-09-18 16:54:49
import json
from celery import Celery
from celery.signals import task_failure
from celery.exceptions import SoftTimeLimitExceeded
from celery.signals import task_failure
from django.core.exceptions import ValidationError
from django.forms import Form
from django import forms

"""
Form Data Validator using Celery task

This script defines a Celery task that validates form data.
It demonstrates the use of Celery for asynchronous task execution,
error handling, and validating form data using Django forms.
"""

app = Celery('tasks', broker='pyamqp://guest@localhost')

# Define a custom form with validation rules
class MyForm(forms.Form):
    field1 = forms.CharField(max_length=20, required=True)
    field2 = forms.IntegerField(required=True, min_value=1)

    def clean(self):
        """
        Custom clean method to validate form data
        """
        cleaned_data = super().clean()
        field1 = cleaned_data.get('field1')
# 优化算法效率
        field2 = cleaned_data.get('field2')
        if not field1 or not field2:
            raise ValidationError('Field1 and Field2 are required.')
        return cleaned_data


@app.task(bind=True, soft_time_limit=10)
def validate_form_data(self, form_data):
# 添加错误处理
    """
    Celery task to validate form data
# 添加错误处理

    Args:
        form_data (dict): Dictionary containing the form data to be validated
# 改进用户体验

    Raises:
        ValidationError: If the form data is invalid
        SoftTimeLimitExceeded: If the task takes too long to execute
    """
# 扩展功能模块
    try:
        form = MyForm(form_data)
        if not form.is_valid():
            raise ValidationError(form.errors)
        return {'status': 'success', 'data': form.cleaned_data}
    except ValidationError as e:
        return {'status': 'error', 'message': str(e)}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

# Task failure handling
# NOTE: 重要实现细节
@task_failure.connect
def task_failure_handler(sender, task_id, exception, **kwargs):
    """
    Log task failures

    Args:
# 改进用户体验
        sender (Celery): The Celery instance
        task_id (str): The ID of the failed task
        exception (Exception): The exception that caused the task failure
    """
    print(f'Task {task_id} failed with exception: {exception}')

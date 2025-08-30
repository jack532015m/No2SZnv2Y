# 代码生成时间: 2025-08-31 02:17:46
import unittest
from celery import Celery
from unittest.mock import patch

# 定义Celery应用
app = Celery('tasks', broker='pyamqp://guest@localhost//')
app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
)

# 定义一个简单的Celery任务
@app.task
def add(x, y):
    """任务用于加法运算"""
    return x + y



class TestCeleryTasks(unittest.TestCase):
    """测试Celery任务的单元测试类"""

    @patch('tasks.add')
    def test_add_task(self, mock_add):
        """测试加法任务"""
        # 设置mock返回值
        mock_add.return_value = 8
        # 调用任务
        result = add(3, 5)
        # 验证任务是否被调用
        mock_add.assert_called_once_with(3, 5)
        # 验证返回值
        self.assertEqual(result, 8)


if __name__ == '__main__':
    """如果直接运行此文件，则执行单元测试"""
    unittest.main()
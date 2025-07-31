# 代码生成时间: 2025-08-01 00:51:42
import os
import unittest
from celery import Celery
from celery import states
from celery.app.base import AppControl
from unittest.mock import patch, MagicMock

# 设置环境变量以便在测试中使用测试数据库
os.environ['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
os.environ['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# 定义Celery应用
app = Celery('tasks', broker=os.environ['CELERY_BROKER_URL'])
app.conf.update(
    result_expires=3600,
    timezone='UTC',
    enable_utc=True,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

# 定义一个Celery任务
@app.task(bind=True)
def add(self, x, y):
    """
    简单的加法任务
    :param self: Celery任务实例
    :param x: 第一个加数
    :param y: 第二个加数
    :return: 两个数的和
    """
    return x + y


# 定义单元测试类
class CeleryTestCase(unittest.TestCase):

    def test_add_task(self):
        """
        测试add任务
        """
        result = add.delay(4, 4)
        self.assertEqual(result.get(), 8)
        self.assertEqual(result.status, states.SUCCESS)

    def test_failed_task(self):
        """
        测试失败的任务
        """
        with patch.object(app.control, 'inspect', MagicMock()) as inspect_mock:
            inspect_mock.apply_async.return_value = {'state': states.FAILURE}
            with self.assertRaises(states.FAILURE):
                add.delay(1, 'a')

    def test_retry_task(self):
        """
        测试重试任务
        """
        with patch.object(app.control, 'inspect', MagicMock()) as inspect_mock:
            inspect_mock.apply_async.side_effect = [states.FAILURE, states.SUCCESS]
            result = add.apply((1, 'b'), throw=True, retry=True)
            self.assertEqual(result.status, states.SUCCESS)

# 运行测试
if __name__ == '__main__':
    unittest.main()
# 代码生成时间: 2025-09-05 05:21:52
import os
from celery import Celery

# 配置Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
app = Celery('your_project')
app.config_from_object('django.conf:settings', namespace='CELERY')

# 定义主题切换的任务
@app.task
def switch_theme(user_id, theme_name):
    '''
    切换用户的主题
    :param user_id: 用户ID
    :param theme_name: 要切换的主题名称
    :return: None
    '''
    try:
        # 模拟数据库操作
        # user = User.objects.get(id=user_id)
        # user.theme = theme_name
        # user.save()
        print(f"User {user_id}'s theme switched to {theme_name}")
    except Exception as e:
        print(f"Error switching theme for user {user_id}: {e}")

# 以下为示例代码，实际项目中应使用Django模型管理用户和主题
if __name__ == '__main__':
    # 测试主题切换功能
    switch_theme.delay(1, 'dark')  # 假设用户ID为1，切换到'dark'主题
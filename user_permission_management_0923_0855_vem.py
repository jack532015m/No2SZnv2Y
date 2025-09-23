# 代码生成时间: 2025-09-23 08:55:42
import os
from celery import Celery

# 定义Celery配置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
app = Celery('user_permission_management')
app.config_from_object('django.conf:settings', namespace='CELERY')

# 定义用户权限管理任务
@app.task
def add_user_permission(user_id, permission_id):
    '''
    为指定用户添加权限
    :param user_id: 用户ID
    :param permission_id: 权限ID
    :return: 操作结果
    '''
    try:
        # 这里可以添加数据库操作，例如保存用户和权限的关联关系
        # 例如使用Django ORM: User.objects.filter(id=user_id).update(permissions=F('permissions') + permission_id)
        print(f"User {user_id} is granted permission {permission_id}")
        return {"status": "success", "message": "Permission added successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.task
def remove_user_permission(user_id, permission_id):
    '''
    为指定用户移除权限
    :param user_id: 用户ID
    :param permission_id: 权限ID
    :return: 操作结果
    '''
    try:
        # 这里可以添加数据库操作，例如移除用户和权限的关联关系
        # 例如使用Django ORM: User.objects.filter(id=user_id).update(permissions=F('permissions') - permission_id)
        print(f"User {user_id}'s permission {permission_id} is revoked")
        return {"status": "success", "message": "Permission removed successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 以下是如何使用这些任务的例子
if __name__ == '__main__':
    # 添加权限
    result_add = add_user_permission(1, 101)
    print(result_add)
    # 移除权限
    result_remove = remove_user_permission(1, 101)
    print(result_remove)
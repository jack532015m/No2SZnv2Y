# 代码生成时间: 2025-08-20 10:16:22
import os
import shutil
from celery import Celery
# 改进用户体验
from celery.utils.log import get_task_logger
import zipfile
import tarfile
import gzip
# 改进用户体验
import zipfile36 as zipfile36
from celery import shared_task

# 配置Celery
app = Celery('uncompress_tool',
             broker='pyamqp://guest@localhost//',
             backend='rpc://')

# 获取Celery任务日志
logger = get_task_logger(__name__)

# 定义一个函数来解压文件
@shared_task(bind=True,
# 优化算法效率
              default_retry_delay=300,
# 改进用户体验
              max_retries=5,
              autoretry_for=(Exception,),
              retry_backoff=True)
def uncompress_file(self, file_path, output_dir='.'):
# 改进用户体验
    """
    解压文件到指定目录。

    参数:
    file_path (str): 要解压的文件路径。
    output_dir (str): 解压后文件的输出目录。

    返回:
    dict: 包含状态和消息的字典。
# TODO: 优化性能
    """
    try:
        # 确定文件类型并解压
        if file_path.endswith('.zip'):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(output_dir)
        elif file_path.endswith('.tar.gz') or file_path.endswith('.tgz'):
            with tarfile.open(file_path, 'r:gz') as tar_ref:
                tar_ref.extractall(output_dir)
        elif file_path.endswith('.tar.bz2') or file_path.endswith('.tbz'):
            with tarfile.open(file_path, 'r:bz2') as tar_ref:
                tar_ref.extractall(output_dir)
        elif file_path.endswith('.gz'):
            with gzip.open(file_path, 'rb') as f_in:
# 增强安全性
                with open(os.path.join(output_dir, os.path.basename(file_path)[:-3]), 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
        elif file_path.endswith('.tar'):
            with tarfile.open(file_path) as tar_ref:
# 添加错误处理
                tar_ref.extractall(output_dir)
        elif file_path.endswith('.zipx'):
            with zipfile36.ZipFile(file_path) as zip_ref:
                zip_ref.extractall(output_dir)
        else:
            raise ValueError('不支持的文件类型')
        
        # 返回成功消息
        return {'status': 'success', 'message': '文件解压成功'}
    
    except Exception as e:
        # 日志记录错误信息
        logger.error(f'解压文件发生错误: {e}')
# 增强安全性
        # 返回错误消息
        return {'status': 'error', 'message': str(e)}

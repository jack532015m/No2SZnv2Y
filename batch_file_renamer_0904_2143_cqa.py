# 代码生成时间: 2025-09-04 21:43:33
import os
from celery import Celery

# Celery配置
app = Celery('batch_file_renamer',
             broker='amqp://guest@localhost//')

# 批量文件重命名任务
@app.task
def rename_files(directory, naming_pattern, dry_run=False):
    """
    批量重命名文件工具。
    
    :param directory: 要重命名文件的目录
    :param naming_pattern: 文件命名格式，例如 'file_{:03d}.ext'
    :param dry_run: 是否为模拟运行，不实际修改文件名
    """
    if not os.path.isdir(directory):
        raise ValueError(f'The directory {directory} does not exist.')

    # 获取目录中的所有文件
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    # 按文件修改时间排序
    files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)))

    # 遍历文件并重命名
    for index, filename in enumerate(files, start=1):
        new_name = naming_pattern.format(index)
        original_path = os.path.join(directory, filename)
        new_path = os.path.join(directory, new_name)
        
        # 检查是否已经存在目标文件名
        if os.path.exists(new_path):
            raise FileExistsError(f'The file {new_path} already exists.')
        
        if dry_run:
            print(f'Would rename {original_path} to {new_path}')
        else:
            os.rename(original_path, new_path)
            print(f'Renamed {original_path} to {new_path}')

# 仅用于演示和测试
if __name__ == '__main__':
    # 假设有一个目录和命名模式
    directory = '/path/to/your/files'
    naming_pattern = 'file_{:03d}.txt'
    # 调用重命名任务
    try:
        rename_files(directory, naming_pattern, dry_run=True)
    except Exception as e:
        print(f'An error occurred: {e}')

# 代码生成时间: 2025-08-02 02:31:24
import os
from celery import Celery

# 配置Celery
app = Celery('batch_file_renamer', broker='pyamqp://guest@localhost//')

# 定义任务函数
@app.task
def rename_files(directory, old_new_extension_mapping):
    """
    批量重命名文件工具。
    
    参数:
        directory (str): 文件所在目录。
        old_new_extension_mapping (dict): 旧文件扩展名到新文件扩展名的映射。
    """
    try:
        for filename in os.listdir(directory):
            old_extension = os.path.splitext(filename)[1]
            if old_extension in old_new_extension_mapping:
                new_extension = old_new_extension_mapping[old_extension]
                new_filename = os.path.splitext(filename)[0] + new_extension
                os.rename(
                    os.path.join(directory, filename),
                    os.path.join(directory, new_filename)
                )
                print(f'Renamed {filename} to {new_filename}')
    except FileNotFoundError:
        print(f'Error: The directory {directory} does not exist.')
    except PermissionError:
        print(f'Error: Permission denied to access the directory {directory}.')
    except Exception as e:
        print(f'An unexpected error occurred: {e}')

# 示例用法
if __name__ == '__main__':
    directory_path = '/path/to/your/files'
    extension_mapping = {
        '.txt': '.md',
        '.py': '.pyw',
    }
    # 启动任务
    rename_files.delay(directory_path, extension_mapping)
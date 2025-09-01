# 代码生成时间: 2025-09-01 17:42:40
import os
import json
from celery import Celery
from celery.utils.log import get_task_logger

# 配置Celery
app = Celery('text_file_analyzer', broker='pyamqp://guest@localhost//')

# 获取任务日志记录器
logger = get_task_logger(__name__)


@app.task(name='analyze_text_file', bind=True)
def analyze_text_file(self, file_path):
    """分析文本文件内容的任务。
    
    :param self: Celery任务实例
    :param file_path: 要分析的文本文件路径
    :return: 分析结果，格式为JSON
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件 {file_path} 不存在。")
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        # 这里可以添加更多的文本分析逻辑
        # 例如：计算单词数量、识别关键词等
        # 假设我们简单地统计单词数量
        word_count = len(content.split())
        # 返回分析结果
        return {'file_path': file_path, 'word_count': word_count}
    except Exception as e:
        # 记录异常信息
        logger.error(f"分析文件 {file_path} 出错：{str(e)}")
        raise


if __name__ == '__main__':
    # 运行Celery worker
    app.worker_main()
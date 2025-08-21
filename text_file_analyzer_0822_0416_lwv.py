# 代码生成时间: 2025-08-22 04:16:50
import os
import re
from celery import Celery
from celery.result import AsyncResult

# 配置Celery
app = Celery('tasks',
             broker='pyamqp://guest@localhost//',
             backend='rpc://')

# 定义任务：分析文本文件内容
@app.task
def analyze_text_file(file_path):
    """
    分析给定文本文件的内容。

    参数:
    - file_path: 文本文件的路径

    返回:
    - dictionary: 包含分析结果
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件 {file_path} 不存在")

        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # 分析文本内容
        result = analyze_content(content)

        return result

    except FileNotFoundError as e:
        # 处理文件不存在错误
        return {"error": str(e)}

    except Exception as e:
        # 处理其他错误
        return {"error": str(e)}


def analyze_content(content):
    """
    分析文本内容。

    参数:
    - content: 文本内容

    返回:
    - dictionary: 包含分析结果
    """
    # 计算单词数量
    word_count = len(re.findall(r'\w+', content))

    # 计算句子数量（假设以句号、问号或感叹号结尾）
    sentence_count = len(re.findall(r'[.?!]', content))

    # 返回分析结果
    return {"word_count": word_count, "sentence_count": sentence_count}

# 示例用法：
if __name__ == '__main__':
    file_path = 'example.txt'
    result = analyze_text_file.delay(file_path)
    print('分析结果:', AsyncResult(result.id).get())
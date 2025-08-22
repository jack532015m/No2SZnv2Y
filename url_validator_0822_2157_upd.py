# 代码生成时间: 2025-08-22 21:57:53
from celery import Celery
from urllib.parse import urlparse
import requests
from typing import Optional

# 初始化Celery应用
app = Celery('url_validator', broker='pyamqp://guest@localhost//')

# 定义一个Celery任务，用于验证URL链接的有效性
@app.task
def validate_url(url: str) -> Optional[str]:
    '''
    验证给定URL链接的有效性。
    
    :param url: 需要验证的URL字符串
    :return: 如果URL有效，返回None；如果无效，返回错误信息
    '''
    # 检查URL是否符合基本的URL格式
    try:
        result = urlparse(url)
        # 如果URL没有协议部分，则视为无效
        if not all([result.scheme, result.netloc]):
            return f'Invalid URL: {url}'
    except ValueError:
        return f'Invalid URL: {url}'
    
    # 使用requests库发送HTTP HEAD请求来验证URL的有效性
    try:
        response = requests.head(url, timeout=5)
        # 如果HTTP响应状态码为200-299，则认为URL有效
        if 200 <= response.status_code < 300:
            return None
        else:
            return f'URL returned non-success status code: {response.status_code}'
    except requests.ConnectionError:
        return 'Failed to connect to the URL.'
    except requests.Timeout:
        return 'The request to the URL timed out.'
    except requests.RequestException as e:
        return f'An error occurred: {e}'


if __name__ == '__main__':
    # 测试validate_url函数
    url_to_test = 'https://www.example.com'
    result = validate_url.delay(url_to_test)
    print(f'Validation result for {url_to_test}: {result.get() if result.ready() else "Pending"}')
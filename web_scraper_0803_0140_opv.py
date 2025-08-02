# 代码生成时间: 2025-08-03 01:40:15
import requests
import logging
from bs4 import BeautifulSoup
from celery import Celery
from celery.utils.log import get_task_logger

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = get_task_logger(__name__)

# Celery配置
app = Celery('web_scraper',
             broker='pyamqp://guest@localhost//',
             backend='rpc://')

# 网页抓取函数
@app.task
def scrape_website(url):
    """
    抓取给定URL的网页内容。
    参数:
        url (str): 要抓取的网页的URL。
    返回:
        str: 网页的HTML内容。
    """
    try:
        # 发送HTTP请求获取网页内容
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        # 解析网页内容
        soup = BeautifulSoup(response.text, 'html.parser')
        # 返回网页的HTML内容
        return soup.prettify()
    except requests.RequestException as e:
        # 处理请求异常
        logger.error(f'请求错误: {e}')
        raise
    except Exception as e:
        # 处理其他异常
        logger.error(f'解析错误: {e}')
        raise

# 以下是示例用法
if __name__ == '__main__':
    url = 'http://example.com'
    try:
        html_content = scrape_website.delay(url).get()  # 异步执行并获取结果
        print(html_content)
    except Exception as e:
        print(f'抓取失败: {e}')
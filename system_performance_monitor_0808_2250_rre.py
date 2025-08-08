# 代码生成时间: 2025-08-08 22:50:08
import os
import time
from celery import Celery

# 配置Celery，这里假设Redis作为broker
app = Celery('system_performance_monitor', broker='redis://localhost:6379/0')

@app.task
def monitor_system_performance():
    """监控系统性能的函数。
    
    这个函数会收集系统的性能指标，包括CPU使用率、内存使用情况等，并打印出来。
    """
    try:
        # 收集CPU使用率
        cpu_usage = os.popen('top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\%\)* id.*/\\1/"').read()
        # 收集内存使用情况
        memory_usage = os.popen('free -m')
        for line in memory_usage:
            if 'Mem' in line:
                memory_usage = line
                break
        memory_usage = memory_usage.split()[1] + 'MB used on ' + memory_usage.split()[2] + 'MB total'
        # 打印性能指标
        print(f'CPU Usage: {cpu_usage}%')
        print(f'Memory Usage: {memory_usage}')
    except Exception as e:
        # 错误处理
        print(f'An error occurred while monitoring system performance: {e}')

if __name__ == '__main__':
    # 定时执行系统性能监控任务，这里设定为每5分钟执行一次
    monitor_system_performance.apply_async(countdown=300)
    while True:
        time.sleep(300)  # 每5分钟检查一次
        # 这里可以加入更复杂的逻辑来决定何时执行任务
        monitor_system_performance.apply_async(countdown=300)

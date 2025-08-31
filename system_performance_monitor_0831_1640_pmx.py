# 代码生成时间: 2025-08-31 16:40:48
import os
import psutil
from celery import Celery
from celery.schedules import crontab
from datetime import datetime

# Configuration for Celery
app = Celery('system_performance_monitor',
             broker='amqp://guest:guest@localhost//',
             backend='rpc://')

app.conf.beat_schedule = {
    'monitor_system_performance_every_minute': {
        'task': 'system_performance_monitor.tasks.monitor_performance',
        'schedule': crontab(minute='*/1'),
        'args': ()
    },
}


# Task to monitor system performance
@app.task
def monitor_performance():
    """
    Monitors the system performance by capturing CPU, memory, and disk usage.
    Writes the performance data to a log file with a timestamp.
    """
    try:
        # Gather system performance metrics
        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk_usage = psutil.disk_usage('/')

        # Format the data into a string
        log_data = (
            f"Timestamp: {datetime.now()}
"
            f"CPU Usage: {cpu_usage}%
"
            f"Memory Usage: {memory.percent}%
"
            f"Disk Usage: {disk_usage.percent}%
"
        )

        # Write to log file
        with open('system_performance_log.txt', 'a') as log_file:
            log_file.write(log_data + '
')

    except Exception as e:
        # Log any exceptions that occur during monitoring
        with open('error_log.txt', 'a') as error_file:
            error_file.write(f"Error at {datetime.now()}: {str(e)}
")


# If you want to run the worker for the Celery app
if __name__ == '__main__':
    app.start()
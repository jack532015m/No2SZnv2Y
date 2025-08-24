# 代码生成时间: 2025-08-24 11:21:48
import os
import time
from celery import Celery

"""
System Performance Monitoring Tool
This tool uses Celery to schedule and run periodic tasks for system performance monitoring.
"""

# Configuration
BROKER_URL = 'amqp://localhost//'  # RabbitMQ broker URL
CELERY_RESULT_BACKEND = 'rpc://'

app = Celery('system_monitor', broker=BROKER_URL, backend=CELERY_RESULT_BACKEND)

@app.task
def monitor_system_performance():
    """Monitors system performance metrics."""
    try:
        # Collect system performance metrics
        system_load = os.getloadavg()
        memory_usage = os.popen('free -m').readlines()
        swap_usage = os.popen('free -m').readlines()
        cpu_usage = os.popen('mpstat 1 1').readlines()

        # Process memory usage
        memory_data = memory_usage[1].split()
        memory_total = float(memory_data[1])
        memory_used = float(memory_data[2])
        memory_free = float(memory_data[3])

        # Process swap usage
        swap_data = swap_usage[2].split()
        swap_total = float(swap_data[1])
        swap_used = float(swap_data[2])
        swap_free = float(swap_data[3])

        # Process CPU usage
        cpu_data = cpu_usage[2].split()
        cpu_user = float(cpu_data[1])
        cpu_system = float(cpu_data[3])
        cpu_idle = float(cpu_data[4])

        # Return performance metrics
        return {
            'system_load': system_load,
            'memory_usage': {
                'total': memory_total,
                'used': memory_used,
                'free': memory_free
            },
            'swap_usage': {
                'total': swap_total,
                'used': swap_used,
                'free': swap_free
            },
            'cpu_usage': {
                'user': cpu_user,
                'system': cpu_system,
                'idle': cpu_idle
            }
        }
    except Exception as e:
        # Handle errors and return error message
        return {'error': str(e)}

# Schedule the monitor_system_performance task every 5 minutes
app.conf.beat_schedule = {
    'monitor_system_performance_every_5_minutes': {
        'task': 'system_monitor.monitor_system_performance',
        'schedule': 300.0,  # 5 minutes
    },
}

if __name__ == '__main__':
    app.start()
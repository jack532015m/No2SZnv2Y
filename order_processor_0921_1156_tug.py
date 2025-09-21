# 代码生成时间: 2025-09-21 11:56:53
from celery import Celery
from celery.signals import task_failure
from kombu import Queue, Exchange, Entry
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up your broker and backend URLs
broker_url = 'amqp://localhost//'
result_backend = 'rpc://localhost//'

# Initialize Celery app
app = Celery('order_processor', broker=broker_url, backend=result_backend)

# Define the exchange and queue
exchange = Exchange('order_exchange', type='direct')
order_queue = Queue('order_queue', exchange=exchange, routing_key='order')
app.conf.task_queues = (order_queue,)
app.conf.task_default_queue = 'order_queue'
app.conf.task_default_exchange = 'order_exchange'
app.conf.task_default_routing_key = 'order'

# Example task for processing an order
@app.task(bind=True)
def process_order(self, order_id):
    """Process an order with the given ID."""
    try:
        # Simulate order processing logic
        logger.info(f'Processing order {order_id}')
        # You can add your actual order processing logic here
        # For demonstration, we'll just sleep for a bit
        import time
        time.sleep(2)
        logger.info(f'Order {order_id} processed successfully')
    except Exception as e:
        # Handle any exceptions that occur during order processing
        logger.error(f'Failed to process order {order_id}: {e}')
        raise self.retry(exc=e)

# Signal handler for task failures
@task_failure.connect
def task_failure_handler(sender=None, task_id=None, exception=None, **kwargs):
    """Handle task failures by logging the error."""
    if exception:
        logger.error(f'Task {task_id} failed with exception: {exception}')

# Example usage of the process_order task
if __name__ == '__main__':
    # Process an order with ID 123
    process_order.delay(123)
# 代码生成时间: 2025-08-10 16:57:56
import os
import logging
from celery import Celery
from celery.signals import worker_process_init
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from alembic import command, config as alembic_config
from alembic.util import CommandError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Celery configuration
app = Celery('database_migration_tool',
             broker='amqp://guest:guest@localhost//')
app.conf.update(
    result_backend='rpc://',
    task_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
    result_expires=3600,
)

# Load database migration configuration
migrations_path = os.path.join(os.path.dirname(__file__), 'migrations')
alembic_cfg = alembic_config.Config(os.path.join(migrations_path, 'alembic.ini'))

# Initialize the database engine
def get_database_engine():
    return create_engine(alembic_cfg.get_main_option('sqlalchemy.url'))

# Celery task to perform database migration
@app.task(bind=True)
def migrate_database(self):
    """
    Celery task to perform database migration.
    This task will execute the 'upgrade' command to apply the latest migrations.
    """
    try:
        engine = get_database_engine()
        # Configure Alembic to use the database engine
        alembic_cfg.attributes['engine'] = engine
        # Perform the migration
        command.upgrade(alembic_cfg, 'head')
        logger.info('Database migration completed successfully.')
    except CommandError as ce:
        logger.error('Database migration failed: %s', ce)
        raise self.retry(exc=ce, countdown=60)  # Retry in 60 seconds
    except SQLAlchemyError as se:
        logger.error('Database connection error: %s', se)
        raise self.retry(exc=se, countdown=60)  # Retry in 60 seconds
    except Exception as e:
        logger.error('An unexpected error occurred: %s', e)
        raise self.retry(exc=e, countdown=60)  # Retry in 60 seconds

# Signal handler to initialize the migration process when the worker starts
@worker_process_init.connect
def init_worker_process(**kwargs):
    """
    Signal handler to initialize the migration process when the Celery worker starts.
    This will ensure that the database is migrated when the worker process is initialized.
    """
    migrate_database.delay()

# Example usage:
# app.start()  # Start the Celery worker

if __name__ == '__main__':
    # Run the migration directly for testing purposes
    migrate_database()

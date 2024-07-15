import sys
import os
import logging
import django
from apscheduler.schedulers.blocking import BlockingScheduler
from analyze_platform.operations import DBManager

# Set up Django settings
sys.path.append('/opt/render/project/src')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unky_rick.settings')
django.setup()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize DBManager with a Django model
db_manager = DBManager(django.db.models.Model)

def task():
    """Function to perform scheduled tasks."""
    try:
        db_manager.add_record(column1="value1", column2="value2")
        db_manager.update_record(1, column1="updated_value1")
        db_manager.remove_record(2)
        logger.info(f"Task executed at {datetime.datetime.now()}")
    except Exception as e:
        logger.error(f"Error executing task: {e}")

if __name__ == "__main__":
    logger.info("Starting scheduler...")
    print("Starting scheduler...")  # Console output for visibility
    scheduler = BlockingScheduler()
    scheduler.add_job(task, 'interval', minutes=5)
    logger.info("Scheduler started")
    print("Scheduler started")  # Console output for visibility
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped")
        print("Scheduler stopped")  # Console output for visibility
    except Exception as e:
        logger.error(f"Scheduler encountered an error: {e}")
        print(f"Scheduler encountered an error: {e}")  # Console output for visibility

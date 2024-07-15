from apscheduler.schedulers.blocking import BlockingScheduler
from analyze_platform.operations import DBManager
from django.db import Record
import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db_manager = DBManager(Record)

def task():
    # Example add operation
    db_manager.add_record(column1="value1", column2="value2")
    
    # Example update operation
    db_manager.update_record(1, column1="updated_value1")
    
    # Example remove operation
    db_manager.remove_record(2)

    logger.info(f"Task executed at {datetime.datetime.now()}")

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    # scheduler.add_job(task, 'interval', hours=12)
    scheduler.add_job(task, 'interval', minutes=5)
    logger.info("Scheduler started")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Some error")
        pass

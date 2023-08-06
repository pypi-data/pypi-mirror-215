import logging
from tests.config import Configuration
import datetime as dt
import os

def setup_logger():
    # Configure the logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    
    current_date = dt.datetime.today()
    file_name = f"{current_date.day:02d}-{current_date.month:02d}-{current_date.year}.log"
    log_path = f"{Configuration.ROOT_BASE_PATH}/log"
    # Create a FileHandler and set its formatter
    file_handler = logging.FileHandler(os.path.join(log_path, file_name))
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the FileHandler to the logger
    logger.addHandler(file_handler)

    return logger

def write_log(msg,log_type=None):
    logger = setup_logger()
    # Log messages
    if log_type:
       logger.error(msg)
    else:
       logger.info(msg)


import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
import random
import os



def get_trace_id() -> str:
    traceid = os.getenv("TRACE_ID")
    if traceid:
        traceid = traceid.strip()
    if traceid:
        return traceid
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{ts}-{random.randint(1000, 9999)}"

TRACE_ID = get_trace_id()

class TraceIdFilter(logging.Filter):
    def filter(self, record):
        record.trace_id = TRACE_ID
        return True

def setup_logging(log_folder: str, log_file: str):
    os.makedirs(log_folder, exist_ok= True)
    formatter = logging.Formatter(
        '%(asctime)s | %(trace_id)s | %(name)s | %(levelname)s | %(message)s'
    )

    file_handler = RotatingFileHandler(
        os.path.join(log_folder, f'{log_file}_{TRACE_ID}.log'),
        maxBytes=5*1024*1024,
        backupCount=5
    )

    file_handler.setFormatter(formatter)
    file_handler.addFilter(TraceIdFilter())

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.addFilter(TraceIdFilter())
    
    logger = logging.getLogger()
    logger.addFilter(TraceIdFilter())
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


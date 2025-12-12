import logging
import logging.handlers
import os
import json
import sys
from datetime import datetime

# Define custom logging level HAZMAT
HAZMAT_LEVEL_NUM = 60  # Higher than CRITICAL (50)
logging.addLevelName(HAZMAT_LEVEL_NUM, "HAZMAT")

def hazmat(self, message, *args, **kws):
    if self.isEnabledFor(HAZMAT_LEVEL_NUM):
        self._log(HAZMAT_LEVEL_NUM, message, args, **kws)

logging.Logger.hazmat = hazmat

class JSONFormatter(logging.Formatter):
    """
    Formatter to dump logs as JSON objects.
    """
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcfromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "funcName": record.funcName,
            "lineNo": record.lineno,
            "process": record.process,
        }
        
        # Merge extra fields if any
        if hasattr(record, 'extra_data'):
            log_record.update(record.extra_data)
            
        return json.dumps(log_record)

def setup_logger(name="QuirófanoDigital", log_file="logs/execution.jsonl", level=logging.INFO):
    """
    Configures and returns a logger instance with JSONL output and rotation.
    """
    # Ensure log directory exists
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger

    # Rotating File Handler (10MB limit, keep 5 backups)
    file_handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=10*1024*1024, backupCount=5, encoding='utf-8'
    )
    file_handler.setFormatter(JSONFormatter())
    
    # Console Handler (Standard Output for immediate feedback, structured)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(JSONFormatter())

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

if __name__ == "__main__":
    # Test execution
    log = setup_logger()
    log.info("System initializing...")
    log.warning("Deuda técnica detected in sector 7")
    log.critical("Parser overload!")
    log.hazmat("BIOHAZARD DETECTED: Recursive rm -rf found!")
    print(f"Logger test complete. Check {os.path.abspath('logs/execution.jsonl')}")

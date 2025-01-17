import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(log_file='app.log', level=logging.ERROR, max_size=5 * 1024 * 1024, backup_count=5):
    """
    Set up the logger for logging errors.

    Args:
        log_file (str): Name of the log file.
        level (int): Logging level. Default is logging.ERROR.
        max_size (int): Maximum size of a log file in bytes. Default is 5 MB.
        backup_count (int): Number of backup files to keep. Default is 5.
    Returns:
        Logger: Configured logger instance.
    """
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Configure the logger
    logger = logging.getLogger('error_logger')
    logger.setLevel(level)

    # Set up file handler with rotation
    handler = RotatingFileHandler(log_file, maxBytes=max_size, backupCount=backup_count)
    handler.setLevel(level)

    # Set up log format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Add the handler to the logger
    if not logger.handlers:
        logger.addHandler(handler)

    return logger


import logging
import os
from utils.path_tool import get_abs_path
from datetime import datetime

# Root Directory Logger
LogRoot = get_abs_path("logs")

# Create the logs directory if it doesn't exist
os.makedirs(LogRoot, exist_ok=True)

# Define the default log format
DefaultLogFormat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')

def get_logger(
        name: str = "agent",
        console_level: int = logging.INFO,
        file_level: int = logging.DEBUG,
        log_file = None,
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Set the root logger level to DEBUG
    
    # If the logger already has handlers, return it to avoid adding duplicate handlers
    if logger.handlers:
        return logger
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(DefaultLogFormat)
    logger.addHandler(console_handler)

    # Create file handler if log_file is provided
    if not log_file:
        log_file = os.path.join(LogRoot, f"{name}_{datetime.now().strftime('%Y%m%d')}.log")
    
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(file_level)
    file_handler.setFormatter(DefaultLogFormat)
    logger.addHandler(file_handler)

    return logger


# Quick access to the default logger
logger = get_logger()

if __name__ == "__main__":
    logger.info("This is an info message.")
    logger.error("This is an error message.")
    logger.warning("This is a warning message.")
    logger.debug("This is a debug message.")
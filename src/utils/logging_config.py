# logging_config.py
import logging


def setup_logger():
    # Create a specific logger for your application
    logger = logging.getLogger("poll_matrix_bot")
    logger.setLevel(logging.INFO)  # Set the logging level for your logger

    # Create a FileHandler to log to a file
    file_handler = logging.FileHandler("poll_matrix_bot.log")
    file_handler.setLevel(logging.INFO)

    # Create a StreamHandler to log to the console
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)

    # Create a formatter and set it for both handlers
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    # Add the handlers to your logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    # Prevent this logger from propagating messages to the root logger
    logger.propagate = False

    return logger

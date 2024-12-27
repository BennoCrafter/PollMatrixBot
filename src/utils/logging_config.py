# logging_config.py
import logging


def setup_logger():
    logger = logging.getLogger("lunchy_bot")
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler("lunchy_bot.log")
    file_handler.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    logger.propagate = False

    return logger

import logging
import colorlog

def setup_logger(name, level=logging.INFO):
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    ))
    logger = colorlog.getLogger(name)
    if not logger.handlers:
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger

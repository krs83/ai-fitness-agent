import logging


def setup_logging(level=logging.INFO):
    """Настраивает единое логирование для всего проекта"""

    logging.basicConfig(
        level=level,
        format='%(levelname)s:    %(asctime)s - %(name)s - %(message)s',
        datefmt='%d-%m-%Y %H:%M:%S'
    )

def get_logger(name):
    return logging.getLogger(name)
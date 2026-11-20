import logging
from pathlib import Path


class MaxLevelFilter(logging.Filter):
    def __init__(self, max_level):
        super().__init__()
        self.max_level = max_level

    def filter(self, record):
        return record.levelno < self.max_level


def logger_init():
    dir = Path("logs")
    dir.mkdir(exist_ok=True)

    logger = logging.getLogger("logger")
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    def_handle = logging.FileHandler(dir / "logs.log", encoding="utf-8")
    def_handle.setLevel(logging.INFO)
    def_handle.addFilter(MaxLevelFilter(logging.ERROR))
    def_handle.setFormatter(formatter)

    err_handler = logging.FileHandler(dir / "error_logs.log", encoding="utf-8")
    err_handler.setLevel(logging.ERROR)
    err_handler.setFormatter(formatter)

    logger.addHandler(def_handle)
    logger.addHandler(err_handler)

    return logger

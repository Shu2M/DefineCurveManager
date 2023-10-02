"""Модуль хранения настроечных констант."""
from pathlib import Path
import logging

from source import config


def get_logger():
    """Функция создания и настройки режимов работы и вывода логгера.

    Returns:
        настроенный объект логгера
    """
    logger = logging.getLogger()
    file_handler = logging.FileHandler(
        filename=LOGGER_FILE_PATH,
        mode='a',
    )
    formatter = logging.Formatter(LOGGER_FORMATTER_STRING)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
    return logger


BASE_DIR = Path(__file__).resolve().parent
CONFIG_FILE = config.ConfigTxt(str(BASE_DIR / 'config.txt'))
LOGGER_FILE_PATH = BASE_DIR / 'log.log'
LOGGER_FORMATTER_STRING = (
    '%(asctime)s - '
    + '[%(levelname)s] - '
    + '(%(funcName)s%(lineno)d) - '
    + '%(message)s'
)
LOGGER = get_logger()

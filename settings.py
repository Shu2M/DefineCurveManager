"""Модуль хранения настроечных констант."""
from pathlib import Path

from source import config

BASE_DIR = Path(__file__).resolve().parent
CONFIG_FILE = config.ConfigTxt(str(BASE_DIR / 'config.txt'))
LOGGER_FILE_PATH = BASE_DIR / 'log.log'
LOGGER_FORMATTER_STRING = (
    '%(asctime)s - '
    + '[%(levelname)s] - '
    + '(%(funcName)s%(lineno)d) - '
    + '%(message)s'
)

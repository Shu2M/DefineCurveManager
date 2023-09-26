"""Модуль используемых в программе комманд.

Реализует базовый класс комманд (интерфейс комманд), а так же логику
выполнения других комманд
"""
import abc
import typing

import config

CONFIG_FILE = config.ConfigTxt('config.txt')


class Command(abc.ABC):
    """Абстрактный класс комманды.

    Определяет интерфейс класса для работы с его объектами
    """

    @abc.abstractmethod
    def execute(
        self,
        additional_data: typing.Any,
    ):
        """Метод выполнения логики команды.

        Args:
             additional_data: входные данные

        Raises:
            NotImplementedError: Наследник класса Command должен реализовать
                метод execute
        """
        raise NotImplementedError(
            'Наследник класса Command должен реализовать метод execute',
        )


class SetKeyFilePathCommand(Command):
    """Команда установки пути до k файла."""

    def execute(
        self,
        additional_data: typing.Any,
    ):
        """Метод исполнения команды.

        Args:
            additional_data: строка путь до k файла

        Returns:
            статус, результат команды
        """
        CONFIG_FILE.update(keyfile_path=additional_data)
        return True, None


class ShowKeyFilePathCommand(Command):
    """Команда показа пути до k файла."""

    def execute(
        self,
        additional_data: typing.Any,
    ):
        """Метод исполнения команды.

        Args:
            additional_data: дополнительные данные (не требуются)

        Returns:
            статус, результат команды
        """
        return True, CONFIG_FILE.read('keyfile_path')

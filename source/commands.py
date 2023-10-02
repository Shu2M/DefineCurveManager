"""Модуль используемых в программе комманд.

Реализует базовый класс комманд (интерфейс комманд), а так же логику
выполнения других комманд
"""
import abc
import typing

from source.menus.curve_menu import CurveMenu
from source import exceptions
import settings


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
        settings.CONFIG_FILE.update(keyfile_path=additional_data)
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
        return True, settings.CONFIG_FILE.read('keyfile_path')


class GoToCurveRedactorMenuCommand(Command):
    """Команда перехода в другое меню."""

    def execute(
        self,
        additional_data: typing.Any,
    ):
        """Метод исполнения команды.

        Возвращает в качестве статуса False для того, чтобы информация о
        результате работы команды не обрабатывалась после завершения
        цикла нового вложенного меню CurveRedactorMenu

        Args:
            additional_data: дополнительные данные (не требуются)

        Returns:
            статус, результат команды
        """
        CurveMenu().loop()
        return False, None


class BackMenuCommand(Command):
    """Команда завершения цикла текущего меню."""

    def execute(
        self,
        additional_data: typing.Any,
    ):
        """Метод исполнения команды.

        Args:
            additional_data: дополнительные данные (не требуются)

        Raises:
            ExitException: исключение выхода из цикла меню
        """
        raise exceptions.ExitException


class SetCurveByRange(Command):
    """Команда записи/добавления кривой по укзанному промежутку."""

    def execute(
        self,
        additional_data: typing.Any,
    ):
        """Метод исполнения команды.

        Args:
            additional_data: дополнительные данные

        Returns:
            статус, результат команды
        """
        return True, None


class SetCurveByHand(Command):
    """Команда ручной записи значений кривой в curve."""

    def execute(
        self,
        additional_data: typing.Any,
    ):
        """Метод исполнения команды.

        Args:
            additional_data: дополнительные данные

        Returns:
            статус, результат команды
        """
        return True, None


class SetCurveByLsPrePost(Command):
    """Команда добавления кривой из другого k файла."""

    def execute(
        self,
        additional_data: typing.Any,
    ):
        """Метод исполнения команды.

        Args:
            additional_data: дополнительные данные

        Returns:
            статус, результат команды
        """
        return True, None

"""Модуль используемых в программе комманд.

Реализует базовый класс комманд (интерфейс комманд), а так же логику
выполнения других комманд
"""
import abc
import typing


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

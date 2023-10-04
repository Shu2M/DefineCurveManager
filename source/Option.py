"""Модуль класса опций.

Реализует логику работы с опциями в меню и подменю
"""
import typing

from source.commands.Command import Command
import source.input_output_interface as io_interface


class Option(object):
    """Класс опций."""

    def __init__(
        self,
        name: str,
        command: Command,
        prep_call: typing.Callable = None,
        success_message: str = '{result}',
    ):
        """Дандер метод инициализации объекта класса.

        Args:
             name: название опции
             command: объект комманды с методом execute
             prep_call: функция предварительного подготовки данных
             success_message: сообщение в случае успешного выполнения опции
        """
        self.name = name
        self.command = command
        self.prep_call = prep_call
        self.success_message = success_message

    def execute(self):
        """Метод выполенения опции.

        Запускает выполнение комманды, находящейся в опции и печатает
        результат выполнения этой команды если тот успешно завершился
        """
        additional_data = self.prep_call() if self.prep_call else None
        status, command_result = self.command.execute(
            additional_data=additional_data,
        )

        if status:
            io_interface.print_execute_result(
                self.success_message,
                command_result,
            )

    def __str__(self):
        """Дандер метод для конвертирования объектов в строку.

        Returns:
            Строку с именем объекта Option из атрибута name
        """
        return self.name

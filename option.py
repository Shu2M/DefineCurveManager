"""Модуль класса опций.

Реализует логику работы с опциями в меню и подменю
"""
import typing

import commands


class Option(object):
    """Класс опций."""

    def __init__(
        self,
        name: str,
        command: commands.Command,
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

    def choose(self):
        """Метод выбора опции.

        Запускает выполнение комманды, находящейся в опции
        """
        additional_data = self.prep_call() if self.prep_call else None
        status, command_result = self.command.execute(
            additional_data=additional_data,
        )

        if status:
            print(self.success_message.format(result=command_result))

    def __repr__(self):
        """Дандер метод для конвертирования объектов в строку.

        Returns:
             Строку с описанием объекта Option
        """
        return '\n'.join([
            '{class_name}:'.format(class_name=self.__class__.__name__),
            'name: {name}'.format(name=self.name),
            'command: {command!r}'.format(command=self.command),
            'prep_call: {prep_call}'.format(prep_call=self.prep_call),
            'success_message: {suc_msg}'.format(suc_msg=self.success_message),
        ])

"""Модуль для работы с отображением и вводом информации.

Реализован в виде набора функций для работы с консолью windows
"""
import typing
import sys


def print_execute_result(
    message: str,
    command_result: typing.Any,
):
    """Функция принта в консоль вывода успешно выполненной операции.

    Args:
        message: сообщение которое будет выведено в консоль
        command_result: рузультат работы команды
    """
    sys.stdout.write(message.format(result=command_result))
    sys.stdout.write('\n')
    sys.stdout.write('\nНажмите ENTER для возврата в меню...')
    sys.stdin.readline()

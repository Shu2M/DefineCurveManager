"""Команда добавления новой curve по построчному пользовательскому вводу."""
import typing
import re

import settings
from source.commands.Command import Command


HEADER = '*DEFINE_CURVE_TITLE\n'
PARAMETERS_LINE = '$#    lcid      sidr       sfa       sfo      offa      offo    dattyp     lcint\n'
AXIS_NAME_LINE = '$#                a1                  o1  \n'
END = '*END'


class NewCurveByLineCommand(Command):
    """Комманда добавления новой curve по пользовательскому вводу."""

    def execute(
        self,
        additional_data: typing.Any,
    ):
        """Метод исполнения команды.

        Читает исходный файл и записывает все строки кроме *END, после
        начинает цикл считывания новых элементов, добавляет новую curve
        и переписывает файл

        Args:
            additional_data: именованый кортеж с атрибутами name lcid

        Returns:
            статус, результат команды
        """
        string_keyfile_data = ''
        with open(settings.CONFIG_FILE.read('keyfile_path'), 'r') as keyfile:
            for line in keyfile:
                if not re.match(r'\*END', line):
                    string_keyfile_data += line
                else:
                    break

        string_keyfile_data += HEADER
        string_keyfile_data += additional_data.title + '\n'
        string_keyfile_data += PARAMETERS_LINE
        string_keyfile_data += set_define_curve_arguments(
            additional_data.lcid,
        )
        string_keyfile_data += AXIS_NAME_LINE

        curve_data = get_curve_data()
        for a1, o1 in curve_data:
            string_keyfile_data += ' ' * (20 - len(a1)) + a1
            string_keyfile_data += ' ' * (20 - len(o1)) + o1
            string_keyfile_data += '\n'

        string_keyfile_data += END

        with open(settings.CONFIG_FILE.read('keyfile_path'), 'w') as keyfile:
            keyfile.write(string_keyfile_data)

        return True, None


def set_define_curve_arguments(*args, offset=10) -> str:
    """Функция составления строки значений для keyfile.

    Args:
        *args: значения параметров в порядке добавления
        offset: кол-во символов отведенное для одного значения параметра

    Returns:
        Cтроку, заполненую *args
    """
    args_line = ''
    for arg in args:
        args_line += ' ' * (offset - len(str(arg))) + str(arg)
    return args_line + '\n'


def get_curve_data() -> list:
    """Функция построчного ввода кривой.

    Returns:
        Список вида [[a1_0, o1_0], [a1_1, o1_1], ...]
    """
    curve_data = []
    while True:
        user_input = input().split()[0:2]
        if not user_input:
            break
        elif len(user_input) < 2:
            print('Ввод не соответсвует требуемой длине и не будет записан')
            continue
        curve_data.append(user_input)
    return curve_data

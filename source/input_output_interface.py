"""Модуль для работы с отображением и вводом информации.

Реализован в виде набора функций для работы с консолью windows
"""
import os
import sys
import typing
from collections import namedtuple
from tkinter import filedialog, Tk

import settings


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


def clear_screen():
    """Функция очищения экрана консоли."""
    clear = 'cls' if os.name == 'nt' else 'clear'
    os.system(clear)


def print_options(options: dict):
    """Функция печати названий опций в консоль.

    Печатает в консоль названия опций в формате
    ({номер опции}) {название опции}

    Args:
        options: словарь опций меню
    """
    for shortcut, opt in options.items():
        sys.stdout.write(
            '({shortcut}) {opt}\n'.format(shortcut=shortcut, opt=opt),
        )
    sys.stdout.write('\n')


def select_option(options: dict):
    """Функция выбора только существующей опции.

    При выборе несуществующей опции, повторит запрос ввода

    Args:
        options: словарь опций меню

    Returns:
        объект выбранной опции
    """
    option_key = try_get_user_required_type_input(
        'Выберете вариант действия: ',
        required_type=int,
    )
    while option_key not in options.keys():
        sys.stdout.write('\033[F\033[K')
        option_key = try_get_user_required_type_input(
            'Выбрана несуществующая опция. Выберете другой вариант: ',
            required_type=int,
        )
    sys.stdout.write('\n')
    return options[option_key]


def get_parameterized_user_input_function(**kwargs) -> typing.Callable:
    """Возвращает функцию с параметризированным вводом.

    Args:
        **kwargs: словарь значений, где ключ - имя параметра, а
        значение - кортеж вида (message, required type object)

    Returns:
        Функцию, требуемую для ввода данных для работы команды
    """
    def user_input_function():
        """Функция возвращает необходимые данные для работы команды.

        Returns:
            Именованный кортеж с данными для работы конманды
        """
        UserInput = namedtuple('UserInput', kwargs.keys())
        return UserInput._make([
            get_user_input(msg, required_type=req_type)
            for msg, req_type in kwargs.values()
        ])
    return user_input_function


def get_user_input(label, required=True, required_type=str) -> typing.Any:
    """Функция пользовательского ввода.

    Args:
        label: выводимое собщение перед вводом
        required: флаг окончания пользователького ввода
        required_type: тип, к которому следует привести пользовательский ввод

    Returns:
        значение пользовательского ввода в виде строки
    """
    user_input = try_get_user_required_type_input(
        '{label}: '.format(label=label),
        required_type=required_type,
    )
    while required and not (user_input and isinstance(user_input, required_type)):
        sys.stdout.write('\033[F\033[K')
        user_input = try_get_user_required_type_input(
            'Ввод не выполнен или нельзя преобразовать '
            + 'в требуемый тип. {label}: '.format(label=label),
            required_type=required_type,
        )
    return user_input


def try_get_user_required_type_input(msg, required_type: typing.Type) -> typing.Any:
    """Функция пробует перевести пользовательский ввод в required_type.

        Args:
            msg: сообщение, выводимое при вводе
            required_type: требуемый тип ввода

        Returns:
             значение ввода в требуемом типе
        """
    user_input = input(msg)
    try:
        return required_type(user_input)
    except ValueError:
        return user_input


def get_input_data_by_line(
        max_args_in_line: int = 2,
        required_type: typing.Callable = int,
        msg: str = None,
) -> list[list]:
    """Функция построчного ввода кривой.

    Args:
        max_args_in_line: максимальное кол-во значений в строке
        required_type: требуемый тип ввода
        msg: выводимое сообщение

    Returns:
        Список списков значений построчного ввода в требуемом типе
    """
    if msg:
        print(msg)
    curve_data = []
    while True:
        user_input = input().split()[:max_args_in_line]

        if not user_input:
            break
        elif len(user_input) < max_args_in_line:
            print('Ввод не соответсвует требуемой длине и не будет записан')
            continue

        try:
            for ind, value in enumerate(user_input):
                user_input[ind] = required_type(value)
        except ValueError:
            print(
                'Ввод не соответсвует требуемому типу {type_name} и не '
                'будет записан'.format(type_name=required_type.__name__)
            )
            continue

        curve_data.append(user_input)
    return curve_data


def get_valid_path(label: str) -> str:
    """Функция ввода валидного пути файла.

    Args:
        label: строка с сообщением для пользователя

    Returns:
        Строку пути существующего файла
    """
    path = get_user_input(label)
    while not os.path.exists(path):
        sys.stdout.write('\033[F\033[K')
        path = get_user_input(
            'Файла по указанному пути не существует. '
            '{label}'.format(label=label),
        )
    return path


def get_path_by_file_explorer(
        title: str = 'Open a file',
        initialdir: str = settings.BASE_DIR,
        filetypes: tuple[tuple[str, str]] = (('All files', '*.*'),),
        message: str = ''
) -> str:
    """Функция открывает файловый проводник и возвращает путь.

    Открывает файловый проводник и дает пользователю возможность выбрать
    файл с требуемым расширением

    Args:
        title: заголовок окна менеждера файлов
        initialdir: директория, в которой откроется проводник
        filetypes: типы файлов, которые сможет выбрать пользователь
        message: сообщение, которое увидит пользователь в консоли

    Returns:
        Строку с путем
    """
    root = Tk()
    root.withdraw()

    if message:
        print(message)

    filepath = filedialog.askopenfilename(
        title=title,
        initialdir=initialdir,
        filetypes=filetypes,
    )

    return filepath

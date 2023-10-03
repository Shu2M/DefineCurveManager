"""Модуль для определения методов меню программы.

Определяет набор методов меню
"""
import os
import sys
import typing

from source import exceptions
import settings


class Menu(object):
    """Класс для определения поведения меню."""

    logger = settings.LOGGER

    def __init__(self):
        """Метод инициализации меню."""
        self.options = None
        self.exit = False

    def loop(self):
        """Цикл исполнения меню в консоли."""
        while True:
            clear_screen()
            print_options(self.options)
            selected_option = select_option(self.options)
            try:
                selected_option.execute()
            except exceptions.ExitException:
                break
            except Exception as exception:
                input(
                    'Действие '
                    + '({opt_name})'.format(opt_name=selected_option.name)
                    + ' прервалось на ошибке: '
                    + '{exception}'.format(exception=exception),
                )
                self.logger.error(
                    msg='Действие '
                        + '({opt_name})'.format(opt_name=selected_option.name)
                        + ' прервалось на ошибке: '
                        + '{exception}'.format(exception=exception),
                    exc_info=True,
                )
            else:
                self.logger.info(
                    'Действие '
                    + '<<{opt_name}>> '.format(opt_name=selected_option.name)
                    + 'выполнено',
                )


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

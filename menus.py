"""Модуль для определения вида главного меню и сабменю впрограммы.

Определяет набор инструментов, содержание и поведение меню
"""
import logging
import os
import sys

import commands
import option
import settings


def clear_screen():
    """Функция очищения экрана консоли."""
    clear = 'cls' if os.name == 'nt' else 'clear'
    os.system(clear)


def print_options(options: dict[int: option.Option]):
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


def select_option(options: dict[int: option.Option]) -> option.Option:
    """Функция выбора только существующей опции.

    При выборе несуществующей опции, повторит запрос ввода

    Args:
        options: словарь опций меню

    Returns:
        объект выбранной опции
    """
    option_key = try_get_user_input_as_int('Выберете вариант действия: ')
    while option_key not in options.keys():
        sys.stdout.write('\033[F\033[K')
        option_key = try_get_user_input_as_int(
            'Выбрана несуществующая опция. Выберете другой вариант: ',
        )
    sys.stdout.write('\n')
    return options[option_key]


def try_get_user_input_as_int(msg: str) -> int | str:
    """Функция пробует перевести пользовательский ввод в int.

    Args:
        msg: сообщение, выводимое при вводе

    Returns:
         пользовательский ввод типа int если его можно преобразовать иначе str
    """
    user_input = input(msg)
    try:
        return int(user_input)
    except ValueError:
        return user_input


def get_logger():
    """Функция создания и настройки режимов работы и вывода логгера.

    Returns:
        настроенный объект логгера
    """
    logger = logging.getLogger()
    file_handler = logging.FileHandler(
        filename=settings.LOGGER_FILE_PATH,
        mode='a',
    )
    formatter = logging.Formatter(settings.LOGGER_FORMATTER_STRING)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
    return logger


def get_user_input(label, required=True) -> str:
    """Функция пользовательского ввод.

    Args:
        label: выводимое собщение перед вводом
        required: флаг окончания пользователького ввода

    Returns:
        значение пользовательского ввода в виде строки
    """
    user_input = input('{label}: '.format(label=label)) or None
    while required and not user_input:
        sys.stdout.write('\033[F\033[K')
        user_input = input(
            'Ввод не выполнен. {label}: '.format(label=label),
        ) or None
    return user_input


class Menu(object):
    """Класс для определения поведения меню."""

    logger = get_logger()

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
            except ExitException:
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


class MainMenu(Menu):
    """Класс главного меню приложения."""

    def __init__(self):
        """Метод инициализации вида главного меню приложения."""
        super().__init__()
        self.options = {
            1: option.Option(
                name='Задать расположение k файла',
                command=commands.SetKeyFilePathCommand(),
                prep_call=self._get_keyfile_path,
                success_message='k файл загружен',
            ),
            2: option.Option(
                name='Показать расположение выбранного k файла',
                command=commands.ShowKeyFilePathCommand(),
                success_message='Загруженный k файл находится в:\n{result}',
            ),
            3: option.Option(
                name='Редактировать curve',
                command=commands.GoToCurveRedactorMenuCommand(),
                success_message='',
            ),
            4: option.Option(
                name='Завершить работу приложения',
                command=commands.BackMenuCommand(),
                success_message='',
            ),
        }

    def _get_keyfile_path(self):
        """Метод для возврата пользовательского значения пути до k файла.

        Returns:
            строку путь до k файла
        """
        return get_user_input('Введите путь k файла')


class CurveRedactorMenu(Menu):
    """Класс меню раздела "Редактировать curve"."""

    def __init__(self):
        """Метод инициализации вида меню раздела редактирования программы."""
        super().__init__()
        self.options = {
            1: option.Option(
                name='Задание границ',
                command=commands.SetCurveByRange(),
                success_message='Команда пока не реализованна',
            ),
            2: option.Option(
                name='Добавление вручную по одному',
                command=commands.SetCurveByHand(),
                success_message='Команда пока не реализованна',
            ),
            3: option.Option(
                name='Через выбор элементов в Ls-prePost',
                command=commands.SetCurveByLsPrePost(),
                success_message='Команда пока не реализованна',
            ),
            4: option.Option(
                name='Назад',
                command=commands.BackMenuCommand(),
                success_message='',
            ),
        }


class ExitException(Exception):
    """Класс исключения для выхода из цикла меню."""

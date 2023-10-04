"""Меню добавления новой curve в keyfile."""
from collections import namedtuple

from source.menus.Menu import Menu, get_user_input
from source.Option import Option
from source.commands.BackMenuCommand import BackMenuCommand
from source.commands.NewCurveByRangeCommand import NewCurveByRangeCommand
from source.commands.NewCurveByLineCommand import NewCurveByLineCommand


class NewCurveMenu(Menu):
    """Класс меню создания новой curve."""

    def __init__(self):
        """Метод инициализации."""
        super().__init__()
        self.options = {
            1: Option(
                name='По диапазону',
                command=NewCurveByRangeCommand(),
                prep_call=get_user_range,
                success_message='Новая curve добавлена',
            ),
            2: Option(
                name='Построчный ввод',
                command=NewCurveByLineCommand(),
                prep_call=get_new_curve_info,
                success_message='Новая curve добавлена',
            ),
            3: Option(
                name='Назад',
                command=BackMenuCommand(),
                success_message='',
            ),
        }


def get_user_range():
    """Функция возвращает необходимые данные для работы команды.

    Returns:
        Именованный кортеж с данными для работы конманды
    """
    Range = namedtuple('Range', 'name lcid start stop step')
    return Range(
        get_user_input('Имя новой curve'),
        get_user_input('id новой кривой', required_type=int),
        get_user_input('Начало диапазона', required_type=int),
        get_user_input('Конец диапазона', required_type=int),
        get_user_input('Шаг', required_type=int),
    )


def get_new_curve_info():
    """Функция возвращает необходимые данные для работы команды.

    Returns:
        Именованный кортеж с данными для работы команды
    """
    CurveInfo = namedtuple('CurveInfo', 'name lcid')
    return CurveInfo(
        get_user_input('Имя новой curve'),
        get_user_input('id новой кривой', required_type=int),
    )

"""Модуль определения меню работы с curve."""
from source.menus.menu import Menu
from source import option
from source.commands.set_curve_by_range_command import SetCurveByRange
from source.commands.set_curve_by_hand_command import SetCurveByHand
from source.commands.set_curve_by_lsprepost_command import SetCurveByLsPrePost
from source.commands.back_menu_command import BackMenuCommand


class CurveMenu(Menu):
    """Класс меню раздела "Редактировать curve"."""

    def __init__(self):
        """Метод инициализации вида меню раздела редактирования программы."""
        super().__init__()
        self.options = {
            1: option.Option(
                name='Задание границ',
                command=SetCurveByRange(),
                success_message='Команда пока не реализованна',
            ),
            2: option.Option(
                name='Добавление вручную по одному',
                command=SetCurveByHand(),
                success_message='Команда пока не реализованна',
            ),
            3: option.Option(
                name='Через выбор элементов в Ls-prePost',
                command=SetCurveByLsPrePost(),
                success_message='Команда пока не реализованна',
            ),
            4: option.Option(
                name='Назад',
                command=BackMenuCommand(),
                success_message='',
            ),
        }

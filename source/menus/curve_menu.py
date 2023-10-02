"""Модуль определения меню работы с curve."""
from source.menus.menu import Menu
from source import option
from source.commands import commands


class CurveMenu(Menu):
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

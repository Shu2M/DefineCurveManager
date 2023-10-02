"""Модуль определения меню работы с curve."""
from source.menus.Menu import Menu
from source.Option import Option
from source.commands.SetCurveByRangeCommand import SetCurveByRange
from source.commands.SetCurveByHandCommand import SetCurveByHand
from source.commands.SetCurveByLsprepostCommand import SetCurveByLsPrePost
from source.commands.BackMenuCommand import BackMenuCommand


class CurveMenu(Menu):
    """Класс меню раздела "Редактировать curve"."""

    def __init__(self):
        """Метод инициализации вида меню раздела редактирования программы."""
        super().__init__()
        self.options = {
            1: Option(
                name='Задание границ',
                command=SetCurveByRange(),
                success_message='Команда пока не реализованна',
            ),
            2: Option(
                name='Добавление вручную по одному',
                command=SetCurveByHand(),
                success_message='Команда пока не реализованна',
            ),
            3: Option(
                name='Через выбор элементов в Ls-prePost',
                command=SetCurveByLsPrePost(),
                success_message='Команда пока не реализованна',
            ),
            4: Option(
                name='Назад',
                command=BackMenuCommand(),
                success_message='',
            ),
        }

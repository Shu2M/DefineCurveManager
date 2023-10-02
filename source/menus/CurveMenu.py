"""Модуль определения меню работы с curve."""
from source.menus.Menu import Menu
from source.Option import Option
from source.commands.GoToExtendCurveMenuCommand import GoToExtendCurveMenuCommand
from source.commands.GoToNewCurveMenuCommand import GoToNewCurveMenuCommand
from source.commands.GoToRewriteCurveMenuCommand import GoToRewriteCurveMenuCommand
from source.commands.BackMenuCommand import BackMenuCommand


class CurveMenu(Menu):
    """Класс меню раздела "Редактировать curve"."""

    def __init__(self):
        """Метод инициализации вида меню раздела редактирования программы."""
        super().__init__()
        self.options = {
            1: Option(
                name='Дополнить',
                command=GoToExtendCurveMenuCommand(),
                success_message='',
            ),
            2: Option(
                name='Создать новую',
                command=GoToNewCurveMenuCommand(),
                success_message='',
            ),
            3: Option(
                name='Перезаписать',
                command=GoToRewriteCurveMenuCommand(),
                success_message='',
            ),
            4: Option(
                name='Назад',
                command=BackMenuCommand(),
                success_message='',
            ),
        }

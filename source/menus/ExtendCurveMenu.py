"""Меню расширения curve в keyfile."""
from source.menus.Menu import Menu
from source.Option import Option
from source.commands.BackMenuCommand import BackMenuCommand


class ExtendCurveMenu(Menu):
    """Класс меню расширения существующей кривой."""

    def __init__(self):
        """Метод инициализации."""
        super().__init__()
        self.options = {
            4: Option(
                name='Назад',
                command=BackMenuCommand(),
                success_message='',
            ),
        }
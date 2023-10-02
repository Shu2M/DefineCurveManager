"""Меню перезаписи curve в keyfile."""
from source.menus.Menu import Menu
from source.Option import Option
from source.commands.BackMenuCommand import BackMenuCommand


class RewriteCurveMenu(Menu):
    """Класс меню перезаписи curve."""

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

"""Меню перезаписи curve в keyfile."""
from source.menus.menu import Menu
from source import option
from source.commands.back_menu_command import BackMenuCommand


class RewriteCurveMenu(Menu):
    """Класс меню перезаписи curve."""

    def __init__(self):
        """Метод инициализации."""
        super().__init__()
        self.options = {
            4: option.Option(
                name='Назад',
                command=BackMenuCommand(),
                success_message='',
            ),
        }

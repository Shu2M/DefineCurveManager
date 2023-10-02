"""Меню добавления новой curve в keyfile."""
from source.menus.menu import Menu
from source import option
from source.commands.back_menu_command import BackMenuCommand


class NewCurveMenu(Menu):
    """Класс меню создания новой curve."""

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

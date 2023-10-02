"""Меню добавления новой curve в keyfile."""
from source.menus.Menu import Menu
from source.Option import Option
from source.commands.BackMenuCommand import BackMenuCommand


class NewCurveMenu(Menu):
    """Класс меню создания новой curve."""

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

"""Модуль определения главного меню приложения."""
from source.menus.Menu import Menu
from source.Option import Option
from source.commands.SetKeyfilePathCommand import SetKeyFilePathCommand
from source.commands.ShowKeyfilePathCommand import ShowKeyFilePathCommand
from source.commands.GoToCurveMenuCommand import GoToCurveMenuCommand
from source.commands.BackMenuCommand import BackMenuCommand


class MainMenu(Menu):
    """Класс главного меню приложения."""

    def __init__(self):
        """Метод инициализации вида главного меню приложения."""
        super().__init__()
        self.options = {
            1: Option(
                name='Задать расположение k файла',
                command=SetKeyFilePathCommand(),
                success_message='{result}',
            ),
            2: Option(
                name='Показать расположение выбранного k файла',
                command=ShowKeyFilePathCommand(),
                success_message='Загруженный k файл находится в:\n{result}',
            ),
            3: Option(
                name='Curve',
                command=GoToCurveMenuCommand(),
                success_message='',
            ),
            4: Option(
                name='Завершить работу приложения',
                command=BackMenuCommand(),
                success_message='',
            ),
        }

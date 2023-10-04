"""Модуль определения главного меню приложения."""
from source.menus.Menu import Menu
from source.Option import Option
from source.commands.SetKeyfilePathCommand import SetKeyFilePathCommand
from source.commands.ShowKeyfilePathCommand import ShowKeyFilePathCommand
from source.commands.GoToCurveMenuCommand import GoToCurveMenuCommand
from source.commands.BackMenuCommand import BackMenuCommand
from source.input_output_interface import get_parameterized_user_input_function


class MainMenu(Menu):
    """Класс главного меню приложения."""

    def __init__(self):
        """Метод инициализации вида главного меню приложения."""
        super().__init__()
        self.options = {
            1: Option(
                name='Задать расположение k файла',
                command=SetKeyFilePathCommand(),
                prep_call=get_parameterized_user_input_function(
                    keyfile_path=('Введите путь k файла', str)
                ),
                success_message='k файл загружен',
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

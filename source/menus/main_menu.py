"""Модуль определения главного меню приложения."""
from source.menus import menu
from source import option
from source.commands.set_keyfile_path_command import SetKeyFilePathCommand
from source.commands.show_keyfile_path_command import ShowKeyFilePathCommand
from source.commands.go_to_curve_menu_command import GoToCurveMenuCommand
from source.commands.back_menu_command import BackMenuCommand


class MainMenu(menu.Menu):
    """Класс главного меню приложения."""

    def __init__(self):
        """Метод инициализации вида главного меню приложения."""
        super().__init__()
        self.options = {
            1: option.Option(
                name='Задать расположение k файла',
                command=SetKeyFilePathCommand(),
                prep_call=get_keyfile_path,
                success_message='k файл загружен',
            ),
            2: option.Option(
                name='Показать расположение выбранного k файла',
                command=ShowKeyFilePathCommand(),
                success_message='Загруженный k файл находится в:\n{result}',
            ),
            3: option.Option(
                name='Редактировать curve',
                command=GoToCurveMenuCommand(),
                success_message='',
            ),
            4: option.Option(
                name='Завершить работу приложения',
                command=BackMenuCommand(),
                success_message='',
            ),
        }


def get_keyfile_path():
    """Метод для возврата пользовательского значения пути до k файла.

    Returns:
        строку путь до k файла
    """
    return menu.get_user_input('Введите путь k файла')


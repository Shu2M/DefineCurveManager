"""Модуль определения главного меню приложения."""
from source.menus import menu
from source import option
from source.commands import commands


class MainMenu(menu.Menu):
    """Класс главного меню приложения."""

    def __init__(self):
        """Метод инициализации вида главного меню приложения."""
        super().__init__()
        self.options = {
            1: option.Option(
                name='Задать расположение k файла',
                command=commands.SetKeyFilePathCommand(),
                prep_call=get_keyfile_path,
                success_message='k файл загружен',
            ),
            2: option.Option(
                name='Показать расположение выбранного k файла',
                command=commands.ShowKeyFilePathCommand(),
                success_message='Загруженный k файл находится в:\n{result}',
            ),
            3: option.Option(
                name='Редактировать curve',
                command=commands.GoToCurveRedactorMenuCommand(),
                success_message='',
            ),
            4: option.Option(
                name='Завершить работу приложения',
                command=commands.BackMenuCommand(),
                success_message='',
            ),
        }


def get_keyfile_path():
    """Метод для возврата пользовательского значения пути до k файла.

    Returns:
        строку путь до k файла
    """
    return menu.get_user_input('Введите путь k файла')


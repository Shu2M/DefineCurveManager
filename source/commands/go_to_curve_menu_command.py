"""Команда перехода в меню работы с данными кривой."""
import typing

from source.commands.command import Command
from source.menus.curve_menu import CurveMenu


class GoToCurveMenuCommand(Command):
    """Команда перехода в другое меню."""

    def execute(
        self,
        additional_data: typing.Any,
    ):
        """Метод исполнения команды.

        Возвращает в качестве статуса False для того, чтобы информация о
        результате работы команды не обрабатывалась после завершения
        цикла нового вложенного меню CurveRedactorMenu

        Args:
            additional_data: дополнительные данные (не требуются)

        Returns:
            статус, результат команды
        """
        CurveMenu().loop()
        return False, None

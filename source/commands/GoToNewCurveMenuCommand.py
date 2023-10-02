"""Команда перехода в меню создания новой curve."""
import typing

from source.commands.Command import Command
from source.menus.NewCurveMenu import NewCurveMenu


class GoToNewCurveMenuCommand(Command):
    """Команда перехода в другое меню."""

    def execute(
        self,
        additional_data: typing.Any,
    ):
        """Метод исполнения команды.

        Возвращает в качестве статуса False для того, чтобы информация о
        результате работы команды не обрабатывалась после завершения
        цикла нового вложенного меню

        Args:
            additional_data: дополнительные данные (не требуются)

        Returns:
            статус, результат команды
        """
        NewCurveMenu().loop()
        return False, None
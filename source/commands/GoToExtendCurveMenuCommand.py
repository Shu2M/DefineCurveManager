"""Команда перехода в меню расширения curve."""
import typing

from source.commands.Command import Command
from source.menus.ExtendCurveMenu import ExtendCurveMenu


class GoToExtendCurveMenuCommand(Command):
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
        ExtendCurveMenu().loop()
        return False, None
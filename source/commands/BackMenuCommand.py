"""Комана выхода из цикла меню."""
import typing

from source.commands.Command import Command
from source import exceptions


class BackMenuCommand(Command):
    """Команда завершения цикла текущего меню."""

    def execute(
        self,
        additional_data: typing.Any,
    ):
        """Метод исполнения команды.

        Args:
            additional_data: дополнительные данные (не требуются)

        Raises:
            ExitException: исключение выхода из цикла меню
        """
        raise exceptions.ExitException

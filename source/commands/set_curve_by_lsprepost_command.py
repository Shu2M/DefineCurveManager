"""."""
import typing

from source.commands.command import Command


class SetCurveByLsPrePost(Command):
    """Команда добавления кривой из другого k файла."""

    def execute(
        self,
        additional_data: typing.Any,
    ):
        """Метод исполнения команды.

        Args:
            additional_data: дополнительные данные

        Returns:
            статус, результат команды
        """
        return True, None

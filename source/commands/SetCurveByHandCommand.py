"""."""
import typing

from source.commands.Command import Command


class SetCurveByHand(Command):
    """Команда ручной записи значений кривой в curve."""

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

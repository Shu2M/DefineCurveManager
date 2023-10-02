"""."""
import typing
from source.commands.Command import Command


class SetCurveByRange(Command):
    """Команда записи/добавления кривой по укзанному промежутку."""

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

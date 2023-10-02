"""Реализация команды отображения пути текущего кейфайла."""
import typing

import settings
from source.commands.Command import Command


class ShowKeyFilePathCommand(Command):
    """Команда показа пути до k файла."""

    def execute(
        self,
        additional_data: typing.Any,
    ):
        """Метод исполнения команды.

        Args:
            additional_data: дополнительные данные (не требуются)

        Returns:
            статус, результат команды
        """
        return True, settings.CONFIG_FILE.read('keyfile_path')

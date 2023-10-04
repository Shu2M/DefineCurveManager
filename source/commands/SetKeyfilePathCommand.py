"""Команда установки пути кейфайла в параметр конфиг файла."""
import typing

import settings
from source.commands.Command import Command


class SetKeyFilePathCommand(Command):
    """Команда установки пути до k файла."""

    def execute(
        self,
        additional_data: typing.Any,
    ):
        """Метод исполнения команды.

        Args:
            additional_data: строка путь до k файла

        Returns:
            статус, результат команды
        """
        settings.CONFIG_FILE.update(keyfile_path=additional_data.keyfile_path)
        return True, None

"""Команда установки пути кейфайла в параметр конфиг файла."""
import typing

import settings
from source.commands.Command import Command
from source.input_output_interface import get_path_by_file_explorer


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
        keyfile_path = get_path_by_file_explorer(
            title='Выбор keyfile',
            filetypes=(('Keyfiles', '*.k'),),
        )

        if not keyfile_path:
            return True, 'Кейфайл не выбран'

        settings.CONFIG_FILE.update(keyfile_path=keyfile_path)
        return True, 'Задан новый кейфайл'

"""Команда перезаписи curve по указанному сету."""
import typing
import re

import settings
from source.commands.Command import Command
from source.Keyfile import Keyfile


class SetIntersectionCommand(Command):
    """
    Команда создания кривой пересечения (номер узла, пересекся)
     по двум введенным сетам
    """

    def execute(
        self,
        additional_data: typing.Any,
    ):
        """Метод исполнения команды.

        Args:
            additional_data: именованый кортеж с атрибутами sid1 sid2 title lcid

        Returns:
            статус, результат команды
        """
        
        result = 'good'
        return True, result
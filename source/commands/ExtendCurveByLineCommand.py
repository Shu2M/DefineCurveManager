"""Команда дополнения curve по построчному пользовательскому вводу."""
import typing
import re

import settings
from source.commands.Command import Command
from source.Keyfile import Keyfile
from source.input_output_interface import get_input_data_by_line


class ExtendCurveByLineCommand(Command):
    """Комманда добавления curve по построчному вводу."""

    def execute(
        self,
        additional_data: typing.Any,
    ):
        """Метод исполнения команды.

        Args:
            additional_data: именованый кортеж с атрибутами lcid

        Returns:
            статус, результат команды
        """
        with Keyfile(settings.CONFIG_FILE.read('keyfile_path')) as keyfile:
            for keyword in keyfile.keywords:
                if re.match(r'DEFINE_CURVE', keyword.name):
                    if keyword.lcid == additional_data.lcid:
                        curve_data = get_input_data_by_line()
                        for a1, o1 in curve_data:
                            keyword.a1.append(a1)
                            keyword.o1.append(o1)
                        break
        return True, None

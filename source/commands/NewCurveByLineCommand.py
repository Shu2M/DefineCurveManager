"""Команда добавления новой curve по построчному пользовательскому вводу."""
import typing

import settings
from source.commands.Command import Command
from source.Keyfile import Keyfile
from source.input_output_interface import get_input_data_by_line
from source.keywords.keywords_dispatch_dict import KEYWORDS_DISPATCH_DICT


class NewCurveByLineCommand(Command):
    """Комманда добавления новой curve по пользовательскому вводу."""

    def execute(
        self,
        additional_data: typing.Any,
    ):
        """Метод исполнения команды.

        Args:
            additional_data: именованый кортеж с атрибутами title lcid

        Returns:
            статус, результат команды
        """
        new_curve = KEYWORDS_DISPATCH_DICT['DEFINE_CURVE_TITLE'](
            title=additional_data.title,
            lcid=additional_data.lcid,
        )

        curve_data = get_input_data_by_line()
        for a1, o1 in curve_data:
            new_curve.a1.append(a1)
            new_curve.o1.append(o1)

        with Keyfile(settings.CONFIG_FILE.read('keyfile_path')) as keyfile:
            keyfile.add(new_curve)

        return True, None

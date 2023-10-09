"""Команда добавления новой curve по указанному диапазону."""
import typing

import settings
from source.commands.Command import Command
from source.Keyfile import Keyfile
from source.keywords.keywords_dispatch_dict import KEYWORDS_DISPATCH_DICT


class NewCurveByRangeCommand(Command):
    """Комманда добавления новой curve по указанному диапазону."""

    def execute(
        self,
        additional_data: typing.Any,
    ):
        """Метод исполнения команды.

        Args:
            additional_data: именованый кортеж с атрибутами title lcid start
            stop step

        Returns:
            статус, результат команды
        """
        new_curve = KEYWORDS_DISPATCH_DICT['DEFINE_CURVE_TITLE'](
            title=additional_data.title,
            lcid=additional_data.lcid,
        )

        for a1, o1 in enumerate(range(
                additional_data.start,
                additional_data.stop + 1,
                additional_data.step,
        ), start=1):
            new_curve.a1.append(a1)
            new_curve.o1.append(o1)

        with Keyfile(settings.CONFIG_FILE.read('keyfile_path')) as keyfile:
            keyfile.add(new_curve)

        return True, None

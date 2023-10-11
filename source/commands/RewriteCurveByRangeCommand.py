"""Команда перезаписи curve по указанному диапазону."""
import typing
import re

import settings
from source.commands.Command import Command
from source.Keyfile import Keyfile


class RewriteCurveByRangeCommand(Command):
    """Комманда перезаписи curve по указанному диапазону."""

    def execute(
        self,
        additional_data: typing.Any,
    ):
        """Метод исполнения команды.

        Args:
            additional_data: именованый кортеж с атрибутами lcid start
            stop step

        Returns:
            статус, результат команды
        """
        result = 'Не удалось найти curve по указанному ' \
                 'lcid={lcid}'.format(lcid=additional_data.lcid)
        with Keyfile(settings.CONFIG_FILE.read('keyfile_path')) as keyfile:
            for keyword in keyfile.keywords:
                if re.match(r'DEFINE_CURVE', keyword.name):
                    if keyword.lcid == additional_data.lcid:
                        keyword.a1 = []
                        keyword.o1 = []
                        for a1, o1 in enumerate(range(
                                additional_data.start,
                                additional_data.stop + 1,
                                additional_data.step,
                        ), start=1):
                            keyword.a1.append(a1)
                            keyword.o1.append(o1)
                        result = 'curve с lcid={lcid} ' \
                                 'перезаписана'.format(lcid=additional_data.lcid)
                        break
        return True, result

"""Команда добавления новой curve по указанному диапазону."""
import typing
import re

import settings
from source.commands.Command import Command
from source.Keyfile import Keyfile


class ExtendCurveByRangeCommand(Command):
    """Комманда добавления новой curve по указанному диапазону."""

    def execute(
        self,
        additional_data: typing.Any,
    ):
        """Метод исполнения команды.

        Читает исходный файл и записывает все строки кроме *END, после
        добавляет новую curve по шаблону и переписывает файл

        Args:
            additional_data: именованый кортеж с атрибутами name lcid start
            stop step

        Returns:
            статус, результат команды
        """
        with Keyfile(settings.CONFIG_FILE.read('keyfile_path')) as keyfile:
            for keyword in keyfile.keywords:
                print(keyword.name, bool(re.match(r'DEFINE_CURVE', keyword.name)))
                if re.match(r'DEFINE_CURVE', keyword.name):
                    if keyword.lcid == additional_data.lcid:
                        for a1, o1 in enumerate(range(
                                additional_data.start,
                                additional_data.stop + 1,
                                additional_data.step,
                        ), start=1):
                            keyword.a1.append(a1)
                            keyword.o1.append(o1)
                        break
        return True, None

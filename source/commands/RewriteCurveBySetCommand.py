"""Команда перезаписи curve по указанному сету."""
import typing
import re

import settings
from source.commands.Command import Command
from source.Keyfile import Keyfile
from source.input_output_interface import get_user_input, get_valid_path


class RewriteCurveBySetCommand(Command):
    """Комманда перезаписи curve по указанному сету."""

    def execute(
        self,
        additional_data: typing.Any,
    ):
        """Метод исполнения команды.

        Args:
            additional_data: именованый кортеж с атрибутами lsid

        Returns:
            статус, результат команды
        """
        if get_user_input(
                'Использовать текущий кейфайл?(Y/n)',
                required=False,
        ).strip() in ['Y', 'y', 'yes', '']:
            path = settings.CONFIG_FILE.read('keyfile_path')
        else:
            path = get_valid_path('Путь до кейфайла с set shell')

        sid = get_user_input('sid', required_type=int)

        all_shell_ids = []
        with Keyfile(path) as keyfile:
            for keyword in keyfile.keywords:
                if re.match(r'SET_SHELL_LIST', keyword.name):
                    if keyword.sid == sid:
                        for shell_ids in zip(
                            keyword.eid1,
                            keyword.eid2,
                            keyword.eid3,
                            keyword.eid4,
                            keyword.eid5,
                            keyword.eid6,
                            keyword.eid7,
                            keyword.eid8,
                        ):
                            all_shell_ids += [
                                shell_id for shell_id in shell_ids
                                if shell_id != 0
                            ]

        if not all_shell_ids:
            return True, 'В указанном файле не нашлось set shell c ' \
                         'sid={sid}'.format(sid=sid)

        result = 'Не удалось найти curve по указанному ' \
                 'lcid={lcid}'.format(lcid=additional_data.lcid)
        with Keyfile(settings.CONFIG_FILE.read('keyfile_path')) as keyfile:
            for keyword in keyfile.keywords:
                if re.match(r'DEFINE_CURVE', keyword.name):
                    if keyword.lcid == additional_data.lcid:
                        keyword.a1 = []
                        keyword.o1 = []
                        for a1, o1 in enumerate(all_shell_ids, start=1):
                            keyword.a1.append(a1)
                            keyword.o1.append(o1)
                        result = 'curve с lcid={lcid} ' \
                                 'перезаписана'.format(lcid=additional_data.lcid)
                        break

        return True, result

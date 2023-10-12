"""Команда добавления новой curve по указанному сету."""
import typing
import re

import settings
from source.commands.Command import Command
from source.Keyfile import Keyfile
from source.keywords.keywords_dispatch_dict import KEYWORDS_DISPATCH_DICT
from source.input_output_interface import get_user_input, \
    get_path_by_file_explorer


class NewCurveBySetCommand(Command):
    """Комманда добавления новой curve по указанному сету."""

    def execute(
        self,
        additional_data: typing.Any,
    ):
        """Метод исполнения команды.

        Args:
            additional_data: именованый кортеж с атрибутами title lsid

        Returns:
            статус, результат команды
        """
        new_curve = KEYWORDS_DISPATCH_DICT['DEFINE_CURVE_TITLE'](
            title=additional_data.title,
            lcid=additional_data.lcid,
        )

        if get_user_input(
                'Использовать текущий кейфайл?(Y/n)',
                required=False,
        ).strip() in ['Y', 'y', 'yes', '']:
            path = settings.CONFIG_FILE.read('keyfile_path')
        else:
            path = get_path_by_file_explorer(
                title='Выбор keyfile',
                filetypes=(('Keyfiles', '*.k'),),
                message='Выберете keyfile с нужным set',
            )
            if not path:
                return True, 'Кейфайл не выбран'

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

        for a1, o1 in enumerate(all_shell_ids, start=1):
            new_curve.a1.append(a1)
            new_curve.o1.append(o1)

        with Keyfile(settings.CONFIG_FILE.read('keyfile_path')) as keyfile:
            keyfile.add(new_curve)

        return True, 'Новая curve добавлена'

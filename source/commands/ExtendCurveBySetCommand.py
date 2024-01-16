"""Команда расширения curve по указанному сету."""
import typing
import re

import settings
from source.commands.Command import Command
from source.Keyfile import Keyfile
from source.input_output_interface import get_user_input, \
    get_path_by_file_explorer


class ExtendCurveBySetCommand(Command):
    """Комманда расширения curve по указанному сету."""

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
            path = get_path_by_file_explorer(
                title='Выбор keyfile',
                filetypes=(('Keyfiles', '*.k'),),
                message='Выберете keyfile с нужным set',
            )
            if not path:
                return True, 'Кейфайл не выбран'

        chosen_keyword_set_name = get_user_input('Какой set использовать (shell_list, solid)', required_type=str)
        full_keyword_set_name = 'SET_' + chosen_keyword_set_name.upper()
        sid = get_user_input('sid', required_type=int)

        all_set_ids = []
        with Keyfile(path) as keyfile:
            for keyword in keyfile.keywords:
                if re.match(full_keyword_set_name, keyword.name):
                    if keyword.sid == sid:
                        for set_ids in zip(
                            keyword.eid1,
                            keyword.eid2,
                            keyword.eid3,
                            keyword.eid4,
                            keyword.eid5,
                            keyword.eid6,
                            keyword.eid7,
                            keyword.eid8,
                        ):
                            all_set_ids += [
                                set_id for set_id in set_ids
                                if set_id != 0
                            ]

        if not all_set_ids:
            return True, 'В указанном файле не нашлось set {set_name} c ' \
                         'sid={sid}'.format(sid=sid, set_name=chosen_keyword_set_name)

        result = 'Не удалось найти curve по указанному ' \
                 'lcid={lcid}'.format(lcid=additional_data.lcid)
        with Keyfile(settings.CONFIG_FILE.read('keyfile_path')) as keyfile:
            for keyword in keyfile.keywords:
                if re.match(r'DEFINE_CURVE', keyword.name):
                    if keyword.lcid == additional_data.lcid:
                        start = int(keyword.a1[-1]) + 1
                        for a1, o1 in enumerate(all_set_ids, start=start):
                            keyword.a1.append(a1)
                            keyword.o1.append(o1)
                        result = 'curve с lcid={lcid} ' \
                                 'дополнена'.format(lcid=additional_data.lcid)
                        break

        return True, result

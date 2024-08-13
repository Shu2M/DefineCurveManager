"""Команда перезаписи curve по указанному сету."""
import typing
import re

import settings
from source.commands.Command import Command
from source.Keyfile import Keyfile
from source.keywords.keywords_dispatch_dict import KEYWORDS_DISPATCH_DICT
from source.input_output_interface import get_user_input, \
    get_path_by_file_explorer


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

        chosen_keyword_set_name = get_user_input('Какого типа set использовать (shell_list, solid)', required_type=str)
        full_keyword_set_name = 'SET_' + chosen_keyword_set_name.upper()
        sid1 = get_user_input('sid1', required_type=int)
        sid2 = get_user_input('sid2', required_type=int)
        title = get_user_input('Имя новой кривой', required_type=str)
        lcid = get_user_input('id новой кривой', required_type=str)

        all_set1_ids = get_all_set_ids(full_keyword_set_name, sid1)
        all_set2_ids = get_all_set_ids(full_keyword_set_name, sid2)

        if not all_set1_ids:
            return True, 'В указанном файле не нашлось set {set_name} c ' \
                         'sid={sid}'.format(sid=sid1, set_name=chosen_keyword_set_name)
        elif not all_set2_ids:
            return True, 'В указанном файле не нашлось set {set_name} c ' \
                         'sid={sid}'.format(sid=sid2, set_name=chosen_keyword_set_name)

        intersection_list = []
        for el in all_set1_ids:
            if el in all_set2_ids:
                intersection_list.append(1)
            else:
                intersection_list.append(0)

        new_curve = KEYWORDS_DISPATCH_DICT['DEFINE_CURVE_TITLE'](
            title=title,
            lcid=lcid,
        )

        a1o1 = [[a1, o1] for a1, o1 in zip(all_set1_ids, intersection_list)]
        a1o1.sort(key=lambda line: line[0])

        for a1, o1 in a1o1:
            new_curve.a1.append(a1)
            new_curve.o1.append(o1)

        with Keyfile(settings.CONFIG_FILE.read('keyfile_path')) as keyfile:
            keyfile.add(new_curve)

        return True, 'Новая curve добавлена'


def get_all_set_ids(full_keyword_set_name: str, sid: int) -> list:
    """

    Returns:

    """
    path = settings.CONFIG_FILE.read('keyfile_path')
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
    return all_set_ids

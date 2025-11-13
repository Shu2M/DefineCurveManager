"""Команда создания curve по одному сету с постоянным fiber coef."""
import typing
import re

import settings
from source.commands.Command import Command
from source.Keyfile import Keyfile
from source.keywords.keywords_dispatch_dict import KEYWORDS_DISPATCH_DICT
from source.input_output_interface import get_user_input, \
    get_path_by_file_explorer


class SetFiberRatioCommand(Command):
    """
    Команда создания кривой (номер элемента, объемное содержание волокна)
    по одному введённому сету.
    """

    def execute(
        self,
        additional_data: typing.Any,
    ):
        """Метод исполнения команды.

        Args:
            additional_data: именованый кортеж с атрибутами
                sid, fiber_coef, title, lcid (опционально).

        Returns:
            статус, результат команды
        """

        # Как в рабочем коде: все параметры спрашиваем у пользователя.
        chosen_keyword_set_name = get_user_input(
            "Какого типа set использовать (shell_list, solid)",
            required_type=str,
        )
        full_keyword_set_name = "SET_" + chosen_keyword_set_name.upper()

        sid = get_user_input("sid", required_type=int)

        fiber_coef = get_user_input(
            "объемное содержание волокна для данного set (fiber coef)",
            required_type=float,
        )

        title = get_user_input("Имя новой кривой", required_type=str)
        lcid = get_user_input("id новой кривой", required_type=str)

        all_set_ids = get_all_set_ids(full_keyword_set_name, sid)

        if not all_set_ids:
            return True, "В указанном файле не нашлось set {set_name} c sid={sid}".format(
                sid=sid,
                set_name=chosen_keyword_set_name,
            )

        # Формируем список пар [a1, o1] БЕЗ сортировки.
        # Порядок элементов совпадает с порядком k1–k8 в исходном key-файле.
        a1o1 = [[elem_id, fiber_coef] for elem_id in all_set_ids]

        new_curve = KEYWORDS_DISPATCH_DICT["DEFINE_CURVE_TITLE"](
            title=title,
            lcid=lcid,
        )

        for a1, o1 in a1o1:
            new_curve.a1.append(a1)
            new_curve.o1.append(o1)

        with Keyfile(settings.CONFIG_FILE.read("keyfile_path")) as keyfile:
            keyfile.add(new_curve)

        return True, "Новая curve с fiber coef добавлена"


def get_all_set_ids(full_keyword_set_name: str, sid: int) -> list:
    """
    Возвращает список element id для заданного set.

    Порядок элементов совпадает с порядком, в котором они записаны
    в блоке k1–k8 исходного key-файла.
    """
    path = settings.CONFIG_FILE.read("keyfile_path")
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

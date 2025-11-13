import typing
import re

import settings
from source.commands.Command import Command
from source.Keyfile import Keyfile
from source.keywords.keywords_dispatch_dict import KEYWORDS_DISPATCH_DICT
from source.input_output_interface import get_user_input


class SetFiberRatio(Command):
    """
    Команда создания кривой задания объемного соотношения волокна в элементе
    """

    def execute(
        self,
        additional_data: typing.Any,
    ):
        """Метод исполнения команды.

        Args:
            additional_data: не используется (зарезервировано).

        Returns:
            статус, результат команды
        """

        # Тип set'а (shell_list или solid)
        chosen_keyword_set_name = get_user_input(
            "Какого типа set использовать (shell_list, solid)",
            required_type=str,
        )
        full_keyword_set_name = "SET_" + chosen_keyword_set_name.upper()

        # Количество сетов, для которых задаётся коэффициент
        n_sets = get_user_input(
            "Сколько set'ов будет задано?",
            required_type=int,
        )

        # Список (sid, FiberCoef) в порядке ввода пользователем
        sets_with_coef: list[tuple[int, float]] = []

        for i in range(1, n_sets + 1):
            sid_i = get_user_input(
                f"sid{i}",
                required_type=int,
            )
            coef_i = get_user_input(
                f"объемное содержание волокна для sid{i}",
                required_type=float,
            )
            sets_with_coef.append((sid_i, coef_i))

        title = get_user_input("Имя новой кривой", required_type=str)
        lcid = get_user_input("id новой кривой", required_type=str)

        # Словарь: элемент -> коэффициент волокна
        element_to_ratio: dict[int, float] = {}

        # Обрабатываем set'ы по порядку.
        # Каждый следующий set перебивает коэффициент для общих элементов.
        for sid_i, coef_i in sets_with_coef:
            set_ids_i = get_all_set_ids(full_keyword_set_name, sid_i)
            if not set_ids_i:
                return (
                    True,
                    "В указанном файле не нашлось set {set_name} c sid={sid}".format(
                        sid=sid_i,
                        set_name=chosen_keyword_set_name,
                    ),
                )

            for elem_id in set_ids_i:
                element_to_ratio[elem_id] = coef_i

        if not element_to_ratio:
            return True, "Не удалось получить ни одного элемента из указанных set'ов."

        # Отсортированный список id элементов
        sorted_element_ids = sorted(element_to_ratio.keys())

        # Формируем пары [a1, o1]
        a1o1: list[list[float]] = []
        for elem_id in sorted_element_ids:
            a1o1.append([elem_id, element_to_ratio[elem_id]])

        # Создаем новую curve
        new_curve = KEYWORDS_DISPATCH_DICT["DEFINE_CURVE_TITLE"](
            title=title,
            lcid=lcid,
        )

        # Очищаем предзаполненные значения
        new_curve.a1 = []
        new_curve.o1 = []

        # Добавляем только наши данные: a1 — id элемента, o1 — коэффициент
        for a1, o1 in a1o1:
            new_curve.a1.append(a1)
            new_curve.o1.append(o1)

        # Записываем в key-файл
        keyfile_path = settings.CONFIG_FILE.read("keyfile_path")
        with Keyfile(keyfile_path) as keyfile:
            keyfile.add(new_curve)

        return True, "Новая curve добавлена"


def get_all_set_ids(full_keyword_set_name: str, sid: int) -> list[int]:
    """
    Возвращает список всех element id для keyword'ов
    с заданным именем и sid в key-файле.

    Args:
        full_keyword_set_name: полное имя ключевого слова, например 'SET_SHELL_LIST'.
        sid: идентификатор set'а.

    Returns:
        Список всех element id (без нулевых) для указанного set'а.
    """
    path = settings.CONFIG_FILE.read("keyfile_path")
    all_set_ids: list[int] = []

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
                        for set_id in set_ids:
                            if set_id != 0:
                                all_set_ids.append(set_id)

    return all_set_ids

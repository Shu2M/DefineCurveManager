"""Модуль реализации класса кейворда DEFINE_CURVE_(TITLE)."""
from source.keywords.KeywordAbstract import KeywordAbstract


class Curve(KeywordAbstract):
    """Класс кейворда DEFINE_CURVE_(TITLE)."""

    default_name = 'DEFINE_CURVE'
    title: str = ''
    lcid: int = 0
    sidr: int = 0
    sfa: float = 0.0
    sfo: float = 0.0
    offa: float = 0.0
    offo: float = 0.0
    dattyp: int = 0
    lcint: int = 0
    a1: list[int | float] = []
    o1: list[int | float] = []

    def __init__(self):
        """Метод инициализации объекта."""
        pass

    @property
    def name(self):
        """Свойство, возвращающее имя кейворда."""
        result_name = self.default_name
        if self.title:
            result_name += '_TITLE'
        return result_name

    @property
    def data_below_name(self):
        """Свойство, возвращающее данные, ниже имени кейворда, как строку."""
        result = ''

        if self.title:
            result += self.title + '\n'

        result += '$#    lcid      sidr       sfa       sfo      offa      ' \
                  'offo    dattyp     lcint\n'
        for param_value in [
            self.lcid,
            self.sidr,
            self.sfa,
            self.sfo,
            self.offa,
            self.offo,
            self.dattyp,
            self.lcint,
        ]:
            result += self.format_param_value_to_string(
                param_value=param_value,
                string_cell_width=10,
            )
        result += '\n'

        result += '$#                a1                  o1\n'
        for a1, o1 in zip(self.a1, self.o1):
            result += self.format_param_value_to_string(
                param_value=a1,
                string_cell_width=20,
            )
            result += self.format_param_value_to_string(
                param_value=o1,
                string_cell_width=20,
            )
            result += '\n'

        return result.strip()

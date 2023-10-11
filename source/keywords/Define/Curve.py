"""Модуль реализации класса кейворда DEFINE_CURVE_(TITLE)."""
import re
from dataclasses import dataclass, field

from source.keywords.KeywordAbstract import KeywordAbstract


@dataclass
class Curve(KeywordAbstract):
    """Класс кейворда DEFINE_CURVE_(TITLE)."""

    default_name = 'DEFINE_CURVE'
    param_header_1 = '    lcid      sidr       sfa       sfo      ' \
                     'offa      offo    dattyp     lcint'
    param_header_2 = '                a1                  o1'

    title: str = ''
    lcid: int = 0
    sidr: int = 0
    sfa: float = 0.0
    sfo: float = 0.0
    offa: float = 0.0
    offo: float = 0.0
    dattyp: int = 0
    lcint: int = 0
    a1: list[int | float] = field(default_factory=list)
    o1: list[int | float] = field(default_factory=list)

    def set_from_string(self, keyword_string: str = None):
        """Метод задания значений атрибутов по строке."""
        keyword_data_lines = keyword_string.strip('*\n').split('\n')

        self.title = keyword_data_lines[1] \
            if not re.match(r'\$#', keyword_data_lines[1]) else 'noname curve'

        for data in re.findall(r'(?<=\$#)([^$#]*)', keyword_string):

            if re.match(self.__class__.param_header_1, data):
                params = self._get_param_value_from_string(
                    param_value_string=data.strip('\n').split('\n')[1],
                    string_cell_width=10,
                    param_value_string_length=80,
                )
                self.lcid = int(params[0]) \
                    if params[0] else self.__class__.lcid
                self.sidr = int(params[1]) \
                    if params[1] else self.__class__.sidr
                self.sfa = float(params[2]) \
                    if params[2] else self.__class__.sfa
                self.sfo = float(params[3]) \
                    if params[3] else self.__class__.sfo
                self.offa = float(params[4]) \
                    if params[4] else self.__class__.offa
                self.offo = float(params[5]) \
                    if params[5] else self.__class__.offo
                self.dattyp = int(params[6]) \
                    if params[6] else self.__class__.dattyp
                self.lcint = int(params[7]) \
                    if params[7] else self.__class__.lcint

            elif re.match(self.__class__.param_header_2, data):
                self.a1 = []
                self.o1 = []
                for line in data.strip('\n').split('\n')[1:]:
                    params = self._get_param_value_from_string(
                        param_value_string=line,
                        string_cell_width=20,
                        param_value_string_length=40,
                    )
                    self.a1.append(
                        int(params[0])
                        if params[0].isnumeric() else float(params[0])
                        if params[0] else 0.0
                    )
                    self.o1.append(
                        int(params[1])
                        if params[1].isnumeric() else float(params[1])
                        if params[1] else 0.0
                    )

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

        result += '$#' + self.__class__.param_header_1 + '\n'
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

        result += '$#' + self.__class__.param_header_2 + '\n'
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

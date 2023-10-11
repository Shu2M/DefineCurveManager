"""Модуль реализации класса кейворда SET_SHELL_LIST_(TITLE)."""
import re
from dataclasses import dataclass, field

from source.keywords.KeywordAbstract import KeywordAbstract


@dataclass
class ShellList(KeywordAbstract):
    """Класс кейворда SET_SHELL_LIST_(TITLE)."""

    default_name = 'SET_SHELL_LIST'
    param_header_1 = '     sid       da1       da2       da3       da4'
    param_header_2 = '    eid1      eid2      eid3      eid4      ' \
                     'eid5      eid6      eid7      eid8'

    title: str = ''
    sid: int = 0
    da1: float = 0.0
    da2: float = 0.0
    da3: float = 0.0
    da4: float = 0.0

    eid1: list[int | float] = field(default_factory=list)
    eid2: list[int | float] = field(default_factory=list)
    eid3: list[int | float] = field(default_factory=list)
    eid4: list[int | float] = field(default_factory=list)
    eid5: list[int | float] = field(default_factory=list)
    eid6: list[int | float] = field(default_factory=list)
    eid7: list[int | float] = field(default_factory=list)
    eid8: list[int | float] = field(default_factory=list)

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
                    param_value_string_length=50,
                )
                self.sid = int(params[0]) \
                    if params[0] else self.__class__.sid
                self.da1 = float(params[1]) \
                    if params[1] else self.__class__.da1
                self.da2 = float(params[2]) \
                    if params[2] else self.__class__.da2
                self.da3 = float(params[3]) \
                    if params[3] else self.__class__.da3
                self.da4 = float(params[4]) \
                    if params[4] else self.__class__.da4

            elif re.match(self.__class__.param_header_2, data):
                self.eid1 = []
                self.eid2 = []
                self.eid3 = []
                self.eid4 = []
                self.eid5 = []
                self.eid6 = []
                self.eid7 = []
                self.eid8 = []

                for line in data.strip('\n').split('\n')[1:]:
                    params = self._get_param_value_from_string(
                        param_value_string=line,
                        string_cell_width=10,
                        param_value_string_length=80,
                    )
                    self.eid1.append(int(params[0]) if params[0] else 0)
                    self.eid2.append(int(params[1]) if params[1] else 0)
                    self.eid3.append(int(params[2]) if params[2] else 0)
                    self.eid4.append(int(params[3]) if params[3] else 0)
                    self.eid5.append(int(params[4]) if params[4] else 0)
                    self.eid6.append(int(params[5]) if params[5] else 0)
                    self.eid7.append(int(params[6]) if params[6] else 0)
                    self.eid8.append(int(params[7]) if params[7] else 0)

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
            self.sid,
            self.da1,
            self.da2,
            self.da3,
            self.da4,
        ]:
            result += self.format_param_value_to_string(
                param_value=param_value,
                string_cell_width=10,
            )
        result += '\n'

        result += '$#' + self.__class__.param_header_2 + '\n'
        for (eid1, eid2, eid3, eid4, eid5, eid6, eid7, eid8) in zip(
                self.eid1,
                self.eid2,
                self.eid3,
                self.eid4,
                self.eid5,
                self.eid6,
                self.eid7,
                self.eid8,
        ):
            result += self.format_param_value_to_string(eid1)
            result += self.format_param_value_to_string(eid2)
            result += self.format_param_value_to_string(eid3)
            result += self.format_param_value_to_string(eid4)
            result += self.format_param_value_to_string(eid5)
            result += self.format_param_value_to_string(eid6)
            result += self.format_param_value_to_string(eid7)
            result += self.format_param_value_to_string(eid8)
            result += '\n'

        return result.strip()

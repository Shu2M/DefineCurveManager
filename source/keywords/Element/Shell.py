"""Модуль реализации класса кейворда ELEMENT_SHELL."""
import re
from dataclasses import dataclass, field

from source.keywords.KeywordAbstract import KeywordAbstract

@dataclass
class ElementShell(KeywordAbstract):
    """Класс кейворда ELEMENT_SHELL."""

    default_name = 'ELEMENT_SHELL'
    param_header_1 = '   eid     pid      n1      n2      n3      n4      n5      n6      n7      n8'

    title: str = ''
    eid: list[int | float] = field(default_factory=list)
    pid: list[int | float] = field(default_factory=list)
    n1: list[int | float] = field(default_factory=list)
    n2: list[int | float] = field(default_factory=list)
    n3: list[int | float] = field(default_factory=list)
    n4: list[int | float] = field(default_factory=list)
    n5: list[int | float] = field(default_factory=list)
    n6: list[int | float] = field(default_factory=list)
    n7: list[int | float] = field(default_factory=list)
    n8: list[int | float] = field(default_factory=list)

    def set_from_string(self, keyword_string: str = None):
        """Метод задания значений атрибутов по строке."""

        for data in re.findall(r'(?<=\$#)([^$#]*)', keyword_string):
            for line in data.strip('\n').split('\n')[1:]:
                params = self._get_param_value_from_string(
                    param_value_string=line,
                    string_cell_width=8,
                    param_value_string_length=80,
                )
                self.eid.append(int(params[0]) if params[0] else 0)
                self.pid.append(int(params[1]) if params[1] else 0)
                self.n1.append(int(params[2]) if params[2] else 0)
                self.n2.append(int(params[3]) if params[3] else 0)
                self.n3.append(int(params[4]) if params[4] else 0)
                self.n4.append(int(params[5]) if params[5] else 0)
                self.n5.append(int(params[6]) if params[6] else 0)
                self.n6.append(int(params[7]) if params[7] else 0)
                self.n7.append(int(params[8]) if params[8] else 0)
                self.n8.append(int(params[9]) if params[9] else 0)

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
        for (eid, pid, n1, n2, n3, n4, n5, n6, n7, n8) in zip(
                self.eid,
                self.pid,
                self.n1,
                self.n2,
                self.n3,
                self.n4,
                self.n5,
                self.n6,
                self.n7,
                self.n8,
        ):
            result += self.format_param_value_to_string(eid, string_cell_width=8)
            result += self.format_param_value_to_string(pid, string_cell_width=8)
            result += self.format_param_value_to_string(n1, string_cell_width=8)
            result += self.format_param_value_to_string(n2, string_cell_width=8)
            result += self.format_param_value_to_string(n3, string_cell_width=8)
            result += self.format_param_value_to_string(n4, string_cell_width=8)
            result += self.format_param_value_to_string(n5, string_cell_width=8)
            result += self.format_param_value_to_string(n6, string_cell_width=8)
            result += self.format_param_value_to_string(n7, string_cell_width=8)
            result += self.format_param_value_to_string(n8, string_cell_width=8)
            result += '\n'
        return result.strip()

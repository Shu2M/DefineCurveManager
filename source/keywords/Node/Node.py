"""Модуль реализации класса кейворда NODE."""
import re
from dataclasses import dataclass, field

from source.keywords.KeywordAbstract import KeywordAbstract

@dataclass
class Node(KeywordAbstract):
    """Класс кейворда NODE"""

    default_name = 'NODE'
    param_header_1 = '   nid               x               y               z      tc      rc'

    title: str = ''
    nid: list[int | float] = field(default_factory=list)
    x: list[int | float] = field(default_factory=list)
    y: list[int | float] = field(default_factory=list)
    z: list[int | float] = field(default_factory=list)
    tc: list[int | float] = field(default_factory=list)
    rc: list[int | float] = field(default_factory=list)

    def set_from_string(self, keyword_string: str = None):
        """Метод задания значений атрибутов по строке."""

        for data in re.findall(r'(?<=\$#)([^$#]*)', keyword_string):
            for line in data.strip('\n').split('\n')[1:]:
                params = self._get_param_value_from_string(
                    param_value_string=line,
                    string_cell_width=[8,16,16,16,8,8],
                    param_value_string_length=72,
                )
                self.nid.append(int(params[0]) if params[0] else 0)
                self.x.append(float(params[1]) if params[1] else 0)
                self.y.append(float(params[2]) if params[2] else 0)
                self.z.append(float(params[3]) if params[3] else 0)
                self.tc.append(float(params[4]) if params[4] else 0)
                self.rc.append(float(params[5]) if params[5] else 0)

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
        for (nid, x, y, z, tc, rc) in zip(
                self.nid,
                self.x,
                self.y,
                self.z,
                self.tc,
                self.rc,
        ):
            result += self.format_param_value_to_string(nid, string_cell_width=8)
            result += self.format_param_value_to_string(x, string_cell_width=16)
            result += self.format_param_value_to_string(y, string_cell_width=16)
            result += self.format_param_value_to_string(z, string_cell_width=16)
            result += self.format_param_value_to_string(tc, string_cell_width=8)
            result += self.format_param_value_to_string(rc, string_cell_width=8)
            result += '\n'
        return result.strip()

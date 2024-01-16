"""Модуль реализации класса кейворда SET_SOLID_(TITLE)."""
import re
from dataclasses import dataclass, field

from source.keywords.KeywordAbstract import KeywordAbstract


@dataclass
class ShellList(KeywordAbstract):
    """Класс кейворда SET_SHELL_LIST_(TITLE)."""

    default_name = 'SET_SOLID'
    param_header_1 = '     sid    solver'
    param_header_2 = '      k1        k2        k3        k4        k5        k6        k7        k8'

    title: str = ''
    sid: int = 0
    solver: str = 'MECH'

    k1: list[int | float] = field(default_factory=list)
    k2: list[int | float] = field(default_factory=list)
    k3: list[int | float] = field(default_factory=list)
    k4: list[int | float] = field(default_factory=list)
    k5: list[int | float] = field(default_factory=list)
    k6: list[int | float] = field(default_factory=list)
    k7: list[int | float] = field(default_factory=list)
    k8: list[int | float] = field(default_factory=list)

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
                self.solver = float(params[1]) \
                    if params[1] else self.__class__.solver

            elif re.match(self.__class__.param_header_2, data):
                self.k1 = []
                self.k2 = []
                self.k3 = []
                self.k4 = []
                self.k5 = []
                self.k6 = []
                self.k7 = []
                self.k8 = []

                for line in data.strip('\n').split('\n')[1:]:
                    params = self._get_param_value_from_string(
                        param_value_string=line,
                        string_cell_width=10,
                        param_value_string_length=80,
                    )
                    self.k1.append(int(params[0]) if params[0] else 0)
                    self.k2.append(int(params[1]) if params[1] else 0)
                    self.k3.append(int(params[2]) if params[2] else 0)
                    self.k4.append(int(params[3]) if params[3] else 0)
                    self.k5.append(int(params[4]) if params[4] else 0)
                    self.k6.append(int(params[5]) if params[5] else 0)
                    self.k7.append(int(params[6]) if params[6] else 0)
                    self.k8.append(int(params[7]) if params[7] else 0)

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
            self.solver,
        ]:
            result += self.format_param_value_to_string(
                param_value=param_value,
                string_cell_width=10,
            )
        result += '\n'

        result += '$#' + self.__class__.param_header_2 + '\n'
        for (k1, k2, k3, k4, k5, k6, k7, k8) in zip(
                self.k1,
                self.k2,
                self.k3,
                self.k4,
                self.k5,
                self.k6,
                self.k7,
                self.k8,
        ):
            result += self.format_param_value_to_string(k1)
            result += self.format_param_value_to_string(k2)
            result += self.format_param_value_to_string(k3)
            result += self.format_param_value_to_string(k4)
            result += self.format_param_value_to_string(k5)
            result += self.format_param_value_to_string(k6)
            result += self.format_param_value_to_string(k7)
            result += self.format_param_value_to_string(k8)
            result += '\n'

        return result.strip()

"""Дефолтная реализация класса KeywordAbstract.

Нужна для чтения из кейфайла объектов кейворд, у которых еще нет полноценной
реализации
"""
from dataclasses import dataclass

from source.keywords.KeywordAbstract import KeywordAbstract


@dataclass
class KeywordDefault(KeywordAbstract):
    """Дефолтная реализация класса KeywordAbstract."""

    keyword_string: str = ''

    def set_from_string(self, keyword_string: str):
        """Метод задания значений атрибутов по строке.

        Args:
            keyword_string: строка, содержащая имя кейворда и информацию
            о нем (как в кейфайле)
        """
        self.keyword_string = keyword_string

    @property
    def name(self) -> str:
        """Свойство, возвращающее имя кейворда."""
        keyword_list_string = self.keyword_string.split('\n')
        return keyword_list_string[0].strip('*')

    @property
    def data_below_name(self) -> str:
        """Свойство, возвращающее данные, ниже имени кейворда, как строку."""
        keyword_list_string = self.keyword_string.split('\n')
        return '\n'.join(
            keyword_list_string[1:],
        ).strip() if len(keyword_list_string) > 1 else ''

"""Дефолтная реализация класса KeywordAbstract.

Нужна для чтения из кейфайла объектов кейворд, у которых еще нет полноценной
реализации
"""
from source.keywords.KeywordAbstract import KeywordAbstract


class KeywordDefault(KeywordAbstract):
    """Дефолтная реализация класса KeywordAbstract."""

    def __init__(self, keyword_string: str):
        """Метод инициализации класса.

        Args:
            keyword_string: строка, содержащая имя кейворда и информацию
            о нем (как в кейфайле)
        """
        self.keyword_string = keyword_string

    def __str__(self):
        """Метод представления Keyword'а как строки (как в кейфайле)."""
        output_string = '*' + self.name + '\n'
        if self.data_below_name:
            output_string += self.data_below_name + '\n'
        return output_string

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

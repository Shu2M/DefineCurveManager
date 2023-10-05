"""Модуль с классом для работы с кейфайлом.

Реализован в виде менеджера контекста
"""
import re


class Keyword(object):
    """Вспомогательный класс с которым работает класс Keyfile."""

    def __init__(self, keyword_string: str):
        """Метод инициализации класса.

        Args:
            keyword_string: строка, содержащая имя кейворда и информацию
            о нем (как в кейфайле)
        """
        keyword_list_string = keyword_string.split('\n')
        self.name = keyword_list_string[0].strip('*')
        self.data_below_name = '\n'.join(
            keyword_list_string[1:],
        ).strip() if len(keyword_list_string) > 1 else ''

    def __str__(self):
        """Метод представления Keyword'а как строки (как в кейфайле)."""
        return '*' + self.name + '\n' + self.data_below_name + '\n'


class Keyfile(object):
    """Класс для работы с кейфайлом.

    Работает с блоком with, то есть реализован как менеджер контекста
    Позволяет считывать кейфайл в список объектов кейвордов,
    записывать список кейвордов в новый файл,
    добавлять кейворд в кейфайл,
    удалять кейворд из кейфайла,
    """

    def __init__(self, path: str):
        """Метод инициализации объекта Keyfile.

        Args:
            path путь до кейфайла
        """
        self.path = path
        self.keywords = []

    def __enter__(self):
        """Метод входа в блок with."""
        self.read(self.path)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Метод выхода из блока with."""
        self.write(self.path)

    def __str__(self):
        """Метод строкового отображения кейфайла."""
        return ''.join(str(keyword) for keyword in self.keywords)

    def read(self, path: str):
        """Метод чтения кейфайла в список кейвордов.

        Args:
            path: путь до кейфайла
        """
        with open(path, 'r') as keyfile:
            self._set_keywords_from_string(keyfile.read())

    def write(self, path: str):
        """Метод записи кейфайла в список кейвордов.

        Args:
            path: путь до кейфайла
        """
        with open(path, 'w') as new_keyfile:
            for keyword in self.keywords:
                new_keyfile.write(str(keyword))

    def add(self, keyword, pos: int = -1):
        """Метод добавления новго кейворда в список кейвордов.

        Принимаемый keyword должен иметь строковый атрибут name и
        реализованный метод __str__(), возвращающий строковое
        представление всех данных кейворда

        Args:
            keyword: объект Keyword, который нужно добавить
            pos: позиция нового объекта кейворда в списке кейвордов
        """
        new_keyword = Keyword(str(keyword))
        self.keywords.insert(pos, new_keyword)

    def pop(self, pos: int = -2) -> Keyword:
        """Метод удаления объекта из списка кейвордов.

        Работает аналогично методу pop у списков

        Args:
            pos: позиция объекта кейворда, который нужно удалить

        Returns:
            Возвращает объект кейворда Keyword
        """
        return self.keywords.pop(pos)

    def _set_keywords_from_string(self, keyfile: str):
        """Метод парсит кейфайл, передаваемый в качестве строки.

        Парсит файл, разделяя его на отдельные блоки кейфордов, после чего
        заносит их в класс Keyfile

        Args:
            keyfile: keyfile как цельная строка
        """
        self.keywords = []
        for keyword_string in re.findall(r'(?<=\*)([^*]*)', keyfile):
            self.keywords.append(Keyword(keyword_string))

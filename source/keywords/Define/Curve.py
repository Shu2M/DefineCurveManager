"""Модуль реализации класса кейворда DEFINE_CURVE_(TITLE)."""
from source.keywords.KeywordAbstract import KeywordAbstract


class Curve(KeywordAbstract):
    """Класс кейворда DEFINE_CURVE_(TITLE)."""

    def __init__(self):
        """Метод инициализации объекта."""
        pass

    def __str__(self):
        """Метод приведения объекта к типу str."""
        return None

    @property
    def name(self):
        """Свойство, возвращающее имя кейворда."""
        return None

    @property
    def data_below_name(self):
        """Свойство, возвращающее данные, ниже имени кейворда, как строку."""
        return None

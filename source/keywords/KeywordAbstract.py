"""Абстрактный класс для определения объектов кейвордов."""
import abc


class KeywordAbstract(abc.ABC):
    """Абстрактный класс кейворда."""

    @abc.abstractmethod
    def __init__(self):
        """Метод инициализации объекта."""
        raise NotImplementedError(
            'Метод __init__ потомка класса KeywordAbstract должен быть '
            'реализован'
        )

    @abc.abstractmethod
    def __str__(self):
        """Метод приведения объекта к типу str."""
        raise NotImplementedError(
            'Метод __str__ потомка класса KeywordAbstract должен быть '
            'реализован'
        )

    @property
    @abc.abstractmethod
    def name(self):
        """Свойство, возвращающее имя кейворда."""
        raise NotImplementedError(
            'Свойство name потомка класса KeywordAbstract должно быть '
            'реализовано'
        )

    @property
    @abc.abstractmethod
    def data_below_name(self):
        """Свойство, возвращающее данные, ниже имени кейворда, как строку."""
        raise NotImplementedError(
            'Свойство data_below_name потомка класса KeywordAbstract должно '
            'быть реализовано'
        )

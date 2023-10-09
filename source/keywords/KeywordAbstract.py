"""Абстрактный класс для определения объектов кейвордов."""
import abc
import re


class KeywordAbstract(abc.ABC):
    """Абстрактный класс кейворда."""

    def __str__(self):
        """Метод представления Keyword'а как строки (как в кейфайле)."""
        output_string = '*' + self.name + '\n'
        if self.data_below_name:
            output_string += self.data_below_name + '\n'
        return output_string

    @staticmethod
    def format_param_value_to_string(
            param_value: int | float,
            string_cell_width: int = 10,
    ) -> str:
        """Метод форматирует переданное значение параметра в строку.

        Значение param_value форматируется в строку "        pv", где pv -
        преобразованное в строковый тип значение param_value, а ширина
        строковой "ячейки" (то есть то, сколько символов выделено под запись
        значения параметра) регулируется значением string_cell_width

        Args:
            param_value: значение параметра, которое нужно преобразовать
            string_cell_width: выделенное кол-во символов под запись параметра
            (запись идет справа на лево)

        Returns:
            Строку с записанным значением параметра
        """
        param_value_string = str(param_value)
        diff = string_cell_width - len(param_value_string)

        if diff < 0:
            param_value_string = param_value_string[:diff]
            diff = 0

        return ' ' * diff + param_value_string

    @staticmethod
    def _get_param_value_from_string(
            param_value_string: str,
            string_cell_width: int = 10,
            param_value_string_length: int = 80,
    ) -> list[str]:
        """Метод для разбиения единой строки на подстроки со значениями.

        Args:
            param_value_string: единая строка
            string_cell_width: по сколько символов разбивать строку
            param_value_string_length: какая длина должна быть у принимаемой
            строки с параметрами

        Returns:
            Список строк, в которых находятся значения парамтеров
        """
        if len(param_value_string) < param_value_string_length:
            param_value_string += ' ' * (param_value_string_length - len(param_value_string))
        return list(map(
            lambda value_str: value_str.replace(' ', ''),
            re.findall('.{,' + str(string_cell_width) + '}', param_value_string),
        ))

    @abc.abstractmethod
    def __init__(self, keyword_string: str):
        """Метод инициализации объекта."""
        raise NotImplementedError(
            'Метод __init__ потомка класса KeywordAbstract должен быть '
            'реализован'
        )

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Свойство, возвращающее имя кейворда."""
        raise NotImplementedError(
            'Свойство name потомка класса KeywordAbstract должно быть '
            'реализовано'
        )

    @property
    @abc.abstractmethod
    def data_below_name(self) -> str:
        """Свойство, возвращающее данные, ниже имени кейворда, как строку."""
        raise NotImplementedError(
            'Свойство data_below_name потомка класса KeywordAbstract должно '
            'быть реализовано'
        )

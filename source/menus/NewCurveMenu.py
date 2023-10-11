"""Меню добавления новой curve в keyfile."""
from source.menus.Menu import Menu
from source.Option import Option
from source.commands.BackMenuCommand import BackMenuCommand
from source.commands.NewCurveByRangeCommand import NewCurveByRangeCommand
from source.commands.NewCurveByLineCommand import NewCurveByLineCommand
from source.commands.NewCurveBySetCommand import NewCurveBySetCommand
from source.input_output_interface import get_parameterized_user_input_function


class NewCurveMenu(Menu):
    """Класс меню создания новой curve."""

    def __init__(self):
        """Метод инициализации."""
        super().__init__()
        self.options = {
            1: Option(
                name='По диапазону',
                command=NewCurveByRangeCommand(),
                prep_call=get_parameterized_user_input_function(
                    title=('Имя новой curve', str),
                    lcid=('id новой кривой', int),
                    start=('Начало диапазона', int),
                    stop=('Конец диапазона', int),
                    step=('Шаг', int),
                ),
                success_message='Новая curve добавлена',
            ),
            2: Option(
                name='Построчный ввод',
                command=NewCurveByLineCommand(),
                prep_call=get_parameterized_user_input_function(
                    title=('Имя новой curve', str),
                    lcid=('id новой кривой', int),
                ),
                success_message='Новая curve добавлена',
            ),
            3: Option(
                name='По set shell',
                command=NewCurveBySetCommand(),
                prep_call=get_parameterized_user_input_function(
                    title=('Имя новой curve', str),
                    lcid=('id новой кривой', int),
                ),
                success_message='{result}',
            ),
            4: Option(
                name='Назад',
                command=BackMenuCommand(),
                success_message='',
            ),
        }

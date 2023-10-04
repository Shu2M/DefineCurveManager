"""Меню расширения curve в keyfile."""
from source.menus.Menu import Menu
from source.Option import Option
from source.commands.BackMenuCommand import BackMenuCommand
from source.commands.ExtendCurveByRangeCommand import ExtendCurveByRangeCommand
from source.input_output_interface import get_parameterized_user_input_function


class ExtendCurveMenu(Menu):
    """Класс меню расширения существующей кривой."""

    def __init__(self):
        """Метод инициализации."""
        super().__init__()
        self.options = {
            1: Option(
                name='По диапазону',
                command=ExtendCurveByRangeCommand(),
                prep_call=get_parameterized_user_input_function(
                    title=('Имя новой curve', str),
                    lcid=('id новой кривой', int),
                    start=('Начало диапазона', int),
                    stop=('Конец диапазона', int),
                    step=('Шаг', int),
                ),
                success_message='Curve дополнена',
            ),
            4: Option(
                name='Назад',
                command=BackMenuCommand(),
                success_message='',
            ),
        }

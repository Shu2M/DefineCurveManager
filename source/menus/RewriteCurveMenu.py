"""Меню перезаписи curve в keyfile."""
from source.menus.Menu import Menu
from source.Option import Option
from source.commands.BackMenuCommand import BackMenuCommand
from source.commands.RewriteCurveByRangeCommand import RewriteCurveByRangeCommand
from source.commands.RewriteCurveByLineCommand import RewriteCurveByLineCommand
from source.input_output_interface import get_parameterized_user_input_function


class RewriteCurveMenu(Menu):
    """Класс меню перезаписи curve."""

    def __init__(self):
        """Метод инициализации."""
        super().__init__()
        self.options = {
            1: Option(
                name='По диапазону',
                command=RewriteCurveByRangeCommand(),
                prep_call=get_parameterized_user_input_function(
                    lcid=('id кривой', int),
                    start=('Начало диапазона', int),
                    stop=('Конец диапазона', int),
                    step=('Шаг', int),
                ),
                success_message='Curve перезаписана',
            ),
            2: Option(
                name='Построчный ввод',
                command=RewriteCurveByLineCommand(),
                prep_call=get_parameterized_user_input_function(
                    lcid=('id кривой', int),
                ),
                success_message='Curve перезаписана',
            ),
            3: Option(
                name='Назад',
                command=BackMenuCommand(),
                success_message='',
            ),
        }

"""Команда добавления новой curve по построчному пользовательскому вводу."""
import typing

import settings
from source.commands.Command import Command
from source.Keyfile import Keyfile
from source.input_output_interface import get_input_data_by_line, get_user_input
from source.keywords.keywords_dispatch_dict import KEYWORDS_DISPATCH_DICT


class NewCurveByLineCommand(Command):
    """Комманда добавления новой curve по пользовательскому вводу."""

    def execute(
        self,
        additional_data: typing.Any,
    ):
        """Метод исполнения команды.

        Args:
            additional_data: именованый кортеж с атрибутами title lcid

        Returns:
            статус, результат команды
        """
        new_curve = KEYWORDS_DISPATCH_DICT['DEFINE_CURVE_TITLE'](
            title=additional_data.title,
            lcid=additional_data.lcid,
        )

        if get_user_input(
                'Вводить только o1?(Y/n)',
                required=False,
        ).strip() in ['Y', 'y', 'yes', '']:
            o1_data_temp = get_input_data_by_line(
                msg='Вводите значения o1 построчно. '
                    'Для завершения ввода нажмите '
                    'ENTER на пустой строке',
                max_args_in_line=1,
            )
            o1_data = []
            for o1 in o1_data_temp:
                o1_data += o1

            a1_data = [i + 1 for i in range(len(o1_data))]

            curve_data = [a1_o1 for a1_o1 in zip(a1_data, o1_data)]
        else:
            curve_data = get_input_data_by_line(
                msg='Вводите значения a1 o1 построчно '
                    'через пробел. Для завершения ввода '
                    'нажмите ENTER на пустой строке',
                max_args_in_line=2,
            )
        for a1, o1 in curve_data:
            new_curve.a1.append(a1)
            new_curve.o1.append(o1)

        with Keyfile(settings.CONFIG_FILE.read('keyfile_path')) as keyfile:
            keyfile.add(new_curve)

        return True, None

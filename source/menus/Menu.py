"""Модуль для определения методов меню программы.

Определяет набор методов меню
"""
from source import exceptions
import settings
import source.input_output_interface as io_interface


class Menu(object):
    """Класс для определения поведения меню."""

    logger = settings.LOGGER

    def __init__(self):
        """Метод инициализации меню."""
        self.options = None
        self.exit = False

    def loop(self):
        """Цикл исполнения меню в консоли."""
        while True:
            io_interface.clear_screen()
            io_interface.print_options(self.options)
            selected_option = io_interface.select_option(self.options)
            try:
                selected_option.execute()
            except exceptions.ExitException:
                break
            except Exception as exception:
                input(
                    'Действие '
                    + '({opt_name})'.format(opt_name=selected_option.name)
                    + ' прервалось на ошибке: '
                    + '{exception}'.format(exception=exception),
                )
                self.logger.error(
                    msg='Действие '
                        + '({opt_name})'.format(opt_name=selected_option.name)
                        + ' прервалось на ошибке: '
                        + '{exception}'.format(exception=exception),
                    exc_info=True,
                )
            else:
                self.logger.info(
                    'Действие '
                    + '<<{opt_name}>> '.format(opt_name=selected_option.name)
                    + 'выполнено',
                )

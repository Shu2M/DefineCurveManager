"""Точка входа программы."""
from source.menus import menus


def main():
    """Функция запуска программы."""
    menus.MainMenu().loop()


if __name__ == '__main__':
    main()

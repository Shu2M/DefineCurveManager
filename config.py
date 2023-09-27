"""Модуль для работы с файлом конфигурации.

Предоставляет абстрактный класс менеджера файла конфигурации и его реализации
"""
import abc
import json
import os
import types
import typing

CONFIG_PARAMS_DISPATCH_DICT = types.MappingProxyType({
    'keyfile_path': str,
    'logger_file_path': str,
})


class ConfigFileManager(abc.ABC):
    """Абстрактный класс менеджера файла конфигурации.

    Определяет интерфейс для работы с файлом конфигурации
    """

    def __init__(self, path: str):
        """Дандер метод инициализации объекта ConfigFileManager.

        Args:
            path: путь до файла конфигурации
        """
        self.path = path

    def read(self, key: str) -> typing.Any:
        """Метод чтения параметра по ключю.

        Если не удается найти ключ, вернет None

        Args:
            key: имя параметра в конфиг файле

        Returns:
            значение параметра по ключу key
        """
        param_value = None
        if key in CONFIG_PARAMS_DISPATCH_DICT:
            config_dict = self.read_all()
            param_value = CONFIG_PARAMS_DISPATCH_DICT.get(key)(
                config_dict[key],
            )
        return param_value

    @abc.abstractmethod
    def read_all(self) -> dict:
        """Метод чтения параметров файла конфигурации в словарь.

        Если не удается найти файл, создает дефолтный приватным методом
        _create

        Raises:
            NotImplementedError: Наследник класса ConfigFileManager должен
                реализовать метод read
        """
        raise NotImplementedError(
            'Наследник класса ConfigFileManager должен реализовать метод '
            + 'read',
        )

    @abc.abstractmethod
    def update(self, **kwargs):
        """Метод обновления значений в файле конфигурации.

        Args:
            **kwargs: параметры для обновления или дополнения

        Raises:
            NotImplementedError: Наследник класса ConfigFileManager должен
                реализовать метод read
        """
        raise NotImplementedError(
            'Наследник класса ConfigFileManager должен реализовать метод '
            + 'update',
        )

    def _update_config_params(self, **kwargs) -> dict:
        """Метод обновелния файла конфигурации согласно правилам.

        Метод читает файл конфигруации в словарь с помощью метода self.read,
        обновляет его с помощью метода словаря update

        Args:
            **kwargs: параметры для обновления или дополнения

        Returns:
             обновленный словарь конфиг файла
        """
        config_params = self.read_all()
        for key, new_param_value in kwargs.items():
            if key in CONFIG_PARAMS_DISPATCH_DICT:
                config_params.update(
                    {key: CONFIG_PARAMS_DISPATCH_DICT.get(key)(
                        new_param_value,
                    )},
                )
        return config_params

    @abc.abstractmethod
    def _create(self):
        """Приватный метод создания дефолтного файла конфигруации.

        Raises:
            NotImplementedError: Наследник класса ConfigFileManager должен
                реализовать метод create
        """
        raise NotImplementedError(
            'Наследник класса ConfigFileManager должен реализовать метод '
            + 'create',
        )


class ConfigJson(ConfigFileManager):
    """Реализация класса ConfigFileManager для чтения из json."""

    def read_all(self) -> dict:
        """Метод чтения файла конфигурации в формате json.

        Returns:
            словарь настроек
        """
        if not os.path.exists(self.path):
            self._create()

        with open(self.path, 'r') as config_file:
            config_data = json.load(config_file)

        return config_data

    def update(self, **kwargs):
        """Метод пересохранения файла конфигурации в формате json.

        Дополняет или перезаписывает значения в существующем файле значениями
        из **kwargs, а заетем сохраняет в формате json

        Args:
            **kwargs: параметры для обновления или дополнения
        """
        config_params = self._update_config_params(**kwargs)
        with open(self.path, 'w') as config_file:
            json.dump(config_params, config_file)

    def _create(self):
        """Приватный метод создания дефолтного файла конфигруации .json."""
        with open(self.path, 'w') as config_file:
            default_params_dict = {
                key: '' for key in CONFIG_PARAMS_DISPATCH_DICT
            }
            json.dump(default_params_dict, config_file)


class ConfigTxt(ConfigFileManager):
    """Реализация класса ConfigFileManager для чтения из txt."""

    def read_all(self) -> typing.Any:
        """Метод чтения файла конфигурации в формате txt.

        Returns:
            словарь настроек
        """
        if not os.path.exists(self.path):
            self._create()

        config_data = {}
        with open(self.path, 'r') as config_file:
            for line in config_file.readlines():
                key, param_value = line.strip().split('=')
                config_data.update({key: param_value})

        return config_data

    def update(self, **kwargs):
        """Метод пересохранения файла конфигурации в формате txt.

        Дополняет или перезаписывает значения в существующем файле значениями
        из **kwargs, а заетем сохраняет в формате txt

        Args:
            **kwargs: параметры для обновления или дополнения
        """
        config_params = self._update_config_params(**kwargs)
        with open(self.path, 'w') as config_file:
            for key, param_value in config_params.items():
                config_file.write(
                    '{key}={value}\n'.format(key=key, value=param_value),
                )

    def _create(self):
        """Приватный метод создания дефолтного файла конфигруации .txt."""
        with open(self.path, 'w') as config_file:
            for key, _ in CONFIG_PARAMS_DISPATCH_DICT.items():
                config_file.write(
                    '{key}=\n'.format(key=key),
                )


CONFIG_FILE = ConfigTxt('config.txt')

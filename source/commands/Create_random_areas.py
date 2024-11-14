"""Команда вывода записи элементов."""
import typing
import re
import math
import random
import numpy as np
from scipy.spatial import distance

import settings
from source.commands.Command import Command
from source.Keyfile import Keyfile
from source.keywords.keywords_dispatch_dict import KEYWORDS_DISPATCH_DICT
from source.input_output_interface import get_user_input, \
    get_path_by_file_explorer

class Create_random_areas(Command):
    """Команда вывода записи элементов."""

    def execute(
            self,
            additional_data: typing.Any,
    ):
        """Метод исполнения команды.

                Args:
                    additional_data: именованый кортеж с атрибутами title lsid

                Returns:
                    статус, результат команды
                """

        path = settings.CONFIG_FILE.read('keyfile_path')

        chosen_keyword_set_name = get_user_input('Какого типа set использовать (shell_list, solid)', required_type=str)
        full_keyword_set_name = 'SET_' + chosen_keyword_set_name.upper()
        full_keyword_ELEMENT_name = 'ELEMENT_SHELL'
        full_keyword_NODE_name = 'NODE'
        number_sample = get_user_input('Number of samples in the model', required_type=int)
        sid1 = get_user_input('First sample set number', required_type=int)
        number_areas = get_user_input('Number of areas', required_type=int)
        title = get_user_input('Имя новой кривой', required_type=str)
        lcid = get_user_input('id новой кривой', required_type=str)

        # Load elements and nodes
        elements_keyword = load_elements(full_keyword_ELEMENT_name)
        nodes_keyword = load_nodes(full_keyword_NODE_name)

        # Initialize dictionaries to hold data
        samples_set_coords = {}  # Average coordinates for each sid1 set
        sid2_elements_dict = {}  # Elements in each sid2 set
        sid2_coords_dict = {}  # Average coordinates for each sid2 set
        sorted_sid2_elements_dict = {}  # Sequential numbering for sid2 elements

        # Initialize lists to collect curve data
        a1_list = []
        o1_list = []

        # Initialize the global sequential number counter
        sequential_number = 1

        # Loop over samples
        for sample_index in range(number_sample):
            current_sid = sid1 + sample_index
            sid2_current = sample_index + 1 # Corresponding sid2 SID

            # Get all element IDs for the current sid1 set
            all_set_ids = get_all_set_ids(full_keyword_set_name, current_sid)

            if not all_set_ids:
                return True, f'No set {chosen_keyword_set_name} found with sid={current_sid}'

            # Calculate average coordinates for elements in the current sid1 set
            set_coords = {}
            for element_id in all_set_ids:
                if element_id not in set_coords:
                    node_ids = get_element_nodes(element_id, elements_keyword)
                    avg_coords = calculate_average_coordinates(node_ids, nodes_keyword)
                    if avg_coords is not None and avg_coords.size > 0:
                        set_coords[element_id] = avg_coords
            samples_set_coords[current_sid] = set_coords

            # Randomly select elements for the corresponding sid2 set
            if len(all_set_ids) < number_areas:
                return True, f'Not enough elements in set {chosen_keyword_set_name} with sid={current_sid} to create {number_areas} areas'

            sid2_elements = np.random.choice(all_set_ids, size=number_areas, replace=False).tolist()
            sid2_elements_dict[sid2_current] = sid2_elements

            # Reuse average coordinates from sid1 for sid2 elements
            sid2_set_coords = {}
            for element_id in sid2_elements:
                avg_coords = set_coords.get(element_id)
                if avg_coords is not None:
                    sid2_set_coords[element_id] = avg_coords
            sid2_coords_dict[sid2_current] = sid2_set_coords

            # Assign sequential numbers to elements in the sid2 set
            sorted_element_ids = sorted(sid2_set_coords.keys())
            sorted_sid2_elements = {}
            for element_id in sorted_element_ids:
                sorted_sid2_elements[element_id] = sequential_number
                sequential_number += 1
            sorted_sid2_elements_dict[sid2_current] = sorted_sid2_elements

            # Find closest correspondences between elements in sid1 and sid2
            set1_coords = samples_set_coords[current_sid]
            set2_coords = sid2_set_coords  # Directly use sid2_set_coords
            sorted_sid2_elements = sorted_sid2_elements_dict[sid2_current]

            for element_id1, coords1 in set1_coords.items():
                closest_element_id = find_closest_element(coords1, set2_coords)
                if closest_element_id is not None:
                    sequential_num = sorted_sid2_elements[closest_element_id]
                    a1_list.append(element_id1)
                    o1_list.append(sequential_num)
        # Сортировка данных кривой по первой колонке (a1)
        sorted_curve_data = sorted(zip(a1_list, o1_list), key=lambda x: x[0])

        # Инициализация кривой
        new_curve = KEYWORDS_DISPATCH_DICT['DEFINE_CURVE_TITLE'](
            title=title,
            lcid=lcid,
        )

        # Заполнение кривой отсортированными данными
        for a1, o1 in sorted_curve_data:
            new_curve.a1.append(a1)
            new_curve.o1.append(o1)

        # Add the new curve to the keyfile
        with Keyfile(settings.CONFIG_FILE.read('keyfile_path')) as keyfile:
            keyfile.add(new_curve)

        return True, 'Новая кривая добавлена'


def get_all_set_ids(full_keyword_set_name: str, sid: int) -> list:
    """

    Функция определения элементов в sid1 и sid2

    """
    path = settings.CONFIG_FILE.read('keyfile_path')
    all_set_ids = []

    with Keyfile(path) as keyfile:
        for keyword in keyfile.keywords:
            if re.match(full_keyword_set_name, keyword.name):
                if keyword.sid == sid:
                    for set_ids in zip(
                            keyword.eid1,
                            keyword.eid2,
                            keyword.eid3,
                            keyword.eid4,
                            keyword.eid5,
                            keyword.eid6,
                            keyword.eid7,
                            keyword.eid8,
                    ):
                        all_set_ids += [
                            set_id for set_id in set_ids
                            if set_id != 0
                        ]
    return all_set_ids

def load_elements(full_keyword_ELEMENT_name: str) -> np.ndarray:
    """
    Функция определения элементов и их узлов в виде numpy массива
    """
    path = settings.CONFIG_FILE.read('keyfile_path')
    element_data = []

    with Keyfile(path) as keyfile:
        for keyword in keyfile.keywords:
            if re.match(full_keyword_ELEMENT_name, keyword.name):
                for element_ids in zip(
                        keyword.eid,  # номер элемента
                        keyword.n1,  # 1-й узел
                        keyword.n2,  # 2-й узел
                        keyword.n3,  # 3-й узел
                        keyword.n4,  # 4-й узел
                        keyword.n5,  # 5-й узел
                        keyword.n6,  # 6-й узел
                        keyword.n7,  # 7-й узел
                        keyword.n8,  # 8-й узел
                ):
                    # Добавляем данные элемента в список
                    element_data.append([eid for eid in element_ids])

    # Преобразуем список элементов в numpy массив для удобной работы
    return np.array(element_data)

def load_nodes(full_keyword_NODE_name: str) -> np.ndarray:
    """
    Функция определения узлов и их координат в виде numpy массива
    """
    path = settings.CONFIG_FILE.read('keyfile_path')
    node_data = []

    with Keyfile(path) as keyfile:
        for keyword in keyfile.keywords:
            if re.match(full_keyword_NODE_name, keyword.name):
                for node_ids in zip(
                        keyword.nid,  # номер узла
                        keyword.x,    # координата по x
                        keyword.y,    # координата по y
                        keyword.z,    # координата по z
                ):
                    # Добавляем данные узла в список
                    node_data.append([nid for nid in node_ids])

    # Преобразуем список узлов в numpy массив для удобной работы
    return np.array(node_data)


def get_element_nodes(element_id, elements_array):
    """
    Функция для поиска узлов элемента по его идентификатору с использованием numpy.
    """
    index = np.where(elements_array[:, 0] == element_id)[0]
    if len(index) > 0:
        return elements_array[index[0], 2:]  # Возвращаем узлы n1-n8
    return []


def get_node_coordinates(node_id, nodes_array):
    """
    Функция для поиска координат узла по его идентификатору с использованием numpy.
    """
    index = np.where(nodes_array[:, 0] == node_id)[0]
    if len(index) > 0:
        return nodes_array[index[0], 1:4]  # Возвращаем координаты x, y, z
    return None


def calculate_average_coordinates(node_ids, nodes_array):
    """
    Функция для расчета средних координат элемента на основе узлов.
    """
    coordinates = []

    for node_id in node_ids:
        if node_id != 0:
            coord = get_node_coordinates(node_id, nodes_array)
            if coord is not None:
                coordinates.append(coord)

    coordinates = np.array(coordinates)  # Преобразуем в numpy массив

    if coordinates.size == 0:
        return None

    avg_coords = np.mean(coordinates, axis=0)  # Вычисляем среднее значение по координатам (x, y, z)
    return avg_coords


def find_closest_element(avg_coords, set2_coords):
    """
    Функция для поиска ближайшего элемента из set2_coords к заданным средним координатам avg_coords.
    """
    min_distance = float('inf')
    closest_element_id = None

    for element_id, coords in set2_coords.items():
        dist = distance.euclidean(avg_coords, coords)
        if dist < min_distance:
            min_distance = dist
            closest_element_id = element_id

    return closest_element_id
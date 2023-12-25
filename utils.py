
import datetime
import json

from json import JSONDecodeError

import bson
from pymongo import MongoClient

from pipelines import get_pipeline



def get_data_for_db():
    """
    Декодирует данные файла sample_collection.bson
    :return: декодированные данные для бд
    """

    with open('sample_collection.bson', 'rb') as bson_file:
        data = bson.decode_all(bson_file.read())
        return data


def get_aggregated_data(collection, time_fr, time_to, group_type):
    """
    Получает словарь агрегированных данных
    :param collection: коллеция данных из бд
    :param time_fr: дата начала сортировки
    :param time_to: дата конца сортировки
    :param group_type: тип группировки данных
    :return: словарь агрегированных данных
    """

    formats_for_date = {
        "hour": "%Y-%m-%dT%H",
        "day": "%Y-%m-%d",
        "week": "",
        "month": "%Y-%m"
    }

    aggregated_data = {'dataset': [], 'labels': []}

    for salary in collection.aggregate(get_pipeline(time_fr, time_to, group_type)):
        date_obj = datetime.datetime.strptime(salary["_id"], formats_for_date[group_type])
        iso_obj = datetime.datetime.isoformat(date_obj)
        aggregated_data['dataset'].append(salary['sum_val'])
        aggregated_data['labels'].append(iso_obj)

    return aggregated_data


def check_input_data(collection, input_data):
    """
    Проверка введенного сообщения на корректность формата ввода
    :param collection: коллекция из бд
    :param input_data: введенное сообщение
    :return: сообщение о некорректности или агрегированный массив
    """

    try:
        json_message = json.loads(input_data)
        dt_from = datetime.datetime.strptime(json_message['dt_from'], '%Y-%m-%dT%H:%M:%S')
        dt_to = datetime.datetime.strptime(json_message['dt_upto'], '%Y-%m-%dT%H:%M:%S')
        group = json_message['group_type']

        output_message = get_aggregated_data(collection, dt_from, dt_to, group)

    except JSONDecodeError:
        output_message = """Введенные данные должны быть формата {"dt_from": "2022-10-01T00:00:00", "dt_upto": "2022-11-30T23:59:00", "group_type": "day"}"""
    except Exception:
        output_message = "Введенные данные не являются корректными"

    return output_message


import unittest

import pytest
from pymongo import MongoClient

from pipelines import get_pipeline, group_types
from run_bot import run
from utils import get_aggregated_data, get_data_for_db, check_input_data


class TestUtils(unittest.TestCase):

    def setUp(self):
        self.client = MongoClient('mongodb://127.0.0.1:27017')
        self.db = self.client.newdb
        self.salaries = self.db.salaries
        self.salaries.delete_many({})
        self.salaries.insert_many(get_data_for_db())

    def test_get_pipeline(self):
        time_fr = "2022-09-01T00:00:00"
        time_to = "2022-12-31T23:59:00"
        group = "month"

        expected_data = [
            {
                "$match": {
                    "dt": {'$gte': "2022-09-01T00:00:00", "$lte": "2022-12-31T23:59:00"}
                }
            },
            {
                "$group":
                    {
                        "_id": {"$dateToString": {"date": "$dt", "format": group_types["month"]}},
                        "sum_val": {"$sum": "$value"}
                    }
            },
            {
                "$sort": {"_id": 1}
            },
        ]
        self.assertEqual(get_pipeline(time_fr, time_to, group), expected_data)

    # def test_get_aggregated_data(self):
    #     time_fr = "2022-09-01T00:00:00"
    #     time_to = "2022-12-31T23:59:00"
    #     group = "month"
    #
    #     expected_data = {"dataset": [5906586, 5515874, 5889803, 6092634], "labels": ["2022-09-01T00:00:00", "2022-10-01T00:00:00", "2022-11-01T00:00:00", "2022-12-01T00:00:00"]}
    #     self.assertEqual(get_aggregated_data(self.salaries, time_fr, time_to, group), expected_data)

    def test_check_input_data(self):
        input_data_test_str = "123"
        input_data_test_wrong_dict = {"dt_from": "2022-02-01T00:00", "dt_to": "2022-22"}
        self.assertEqual(check_input_data(self.salaries, input_data_test_str), "Введенные данные не являются корректными")
        self.assertEqual(check_input_data(self.salaries, input_data_test_wrong_dict), "Введенные данные не являются корректными")


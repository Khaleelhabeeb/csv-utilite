import unittest
from unittest.mock import patch, MagicMock
from typing import Iterable, Any, Union, List, Dict, Optional
import csv
import json
from csv_utils.conversion import csv_to_json, json_to_csv

class CSVUtilsTest(unittest.TestCase):

    def test_csv_to_json_records(self):
        data = [['name', 'age', 'city'], ['Alice', 30, 'New York']]
        json_data = csv_to_json(data)
        self.assertEqual(json_data, [{"name": "Alice", "age": 30, "city": "New York"}])

    def test_csv_to_json_split(self):
        data = [['name', 'age', 'city'], ['Alice', 30, 'New York']]
        json_data = csv_to_json(data, orient='split')
        self.assertEqual(json_data, {'headers': ['name', 'age', 'city'], 'values': [['Alice', 30, 'New York']]})

    def test_csv_to_json_index(self):
        data = [['name', 'age', 'city'], ['Alice', 30, 'New York'], ['Bob', 25, 'London']]
        json_data = csv_to_json(data, orient='index')
        self.assertEqual(json_data, {0: ['Alice', 30, 'New York'], 1: ['Bob', 25, 'London']})

    def test_csv_to_json_columns(self):
        data = [['Alice', 30, 'New York'], ['Bob', 25, 'London']]
        json_data = csv_to_json(data, headers=['name', 'age', 'city'], orient='columns')
        self.assertEqual(json_data, {'name': ['Alice', 'Bob'], 'age': [30, 25], 'city': ['New York', 'London']})

    def test_csv_to_json_values(self):
        data = [['Alice', 30, 'New York'], ['Bob', 25, 'London']]
        json_data = csv_to_json(data, orient='values')
        self.assertEqual(json_data, [['Alice', 30, 'New York'], ['Bob', 25, 'London']])

    def test_csv_to_json_invalid_orient(self):
        data = [['name', 'age', 'city'], ['Alice', 30, 'New York']]
        with self.assertRaises(ValueError):
            csv_to_json(data, orient='invalid')

    def test_json_to_csv_list_records(self):
        data = [{"name": "Alice", "age": 30, "city": "New York"}]
        csv_data = json_to_csv(data)
        expected_data = [['name', 'age', 'city'], ['Alice', 30, 'New York']]
        self.assertEqual(csv_data, expected_data)

    def test_json_to_csv_list_custom_headers(self):
        data = [{"name": "Alice", "age": 30, "city": "New York"}]
        headers = ['FullName', 'YearsOld', 'Location']
        csv_data = json_to_csv(data, headers=headers)
        expected_data = [['FullName', 'YearsOld', 'Location'], ['Alice', 30, 'New York']]
        self.assertEqual(csv_data, expected_data)

if __name__ == '__main__':
    unittest.main()
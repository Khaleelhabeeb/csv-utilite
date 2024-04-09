import unittest
from io import StringIO
from typing import List, Dict, Any

from csv_utilite.conversion import csv_to_json, json_to_csv

class TestCsvJsonConversion(unittest.TestCase):
    def test_csv_to_json_records(self):
        csv_data = [
            ["name", "age", "city"],
            ["John", "30", "New York"],
            ["Jane", "25", "Los Angeles"],
            ["Bob", "40", "Chicago"],
        ]
        expected_json = [
            {"name": "John", "age": "30", "city": "New York"},
            {"name": "Jane", "age": "25", "city": "Los Angeles"},
            {"name": "Bob", "age": "40", "city": "Chicago"},
        ]
        result = csv_to_json(csv_data)
        self.assertEqual(result, expected_json)

    def test_csv_to_json_split(self):
        csv_data = [
            ["name", "age", "city"],
            ["John", "30", "New York"],
            ["Jane", "25", "Los Angeles"],
            ["Bob", "40", "Chicago"],
        ]
        expected_json = {
            "headers": ["name", "age", "city"],
            "values": [["John", "30", "New York"], ["Jane", "25", "Los Angeles"], ["Bob", "40", "Chicago"]],
        }
        result = csv_to_json(csv_data, orient="split")
        self.assertEqual(result, expected_json)

    def test_csv_to_json_index(self):
        csv_data = [
            ["name", "age", "city"],
            ["John", "30", "New York"],
            ["Jane", "25", "Los Angeles"],
            ["Bob", "40", "Chicago"],
        ]
        expected_json = {
            0: ["John", "30", "New York"],
            1: ["Jane", "25", "Los Angeles"],
            2: ["Bob", "40", "Chicago"],
        }
        result = csv_to_json(csv_data, orient="index")
        self.assertEqual(result, expected_json)

    def test_json_to_csv_list(self):
        json_data = [
            {"name": "John", "age": "30", "city": "New York"},
            {"name": "Jane", "age": "25", "city": "Los Angeles"},
            {"name": "Bob", "age": "40", "city": "Chicago"},
        ]
        expected_csv = [
            ["name", "age", "city"],
            ["John", "30", "New York"],
            ["Jane", "25", "Los Angeles"],
            ["Bob", "40", "Chicago"],
        ]
        result = json_to_csv(json_data)
        self.assertEqual(result, expected_csv)

    def test_json_to_csv_dict(self):
        json_data = {
            "John": {"name": "John", "age": "30", "city": "New York"},
            "Jane": {"name": "Jane", "age": "25", "city": "Los Angeles"},
            "Bob": {"name": "Bob", "age": "40", "city": "Chicago"},
        }
        expected_csv = [
            ["name", "age", "city"],
            ["John", "30", "New York"],
            ["Jane", "25", "Los Angeles"],
            ["Bob", "40", "Chicago"],
        ]
        result = json_to_csv(json_data)
        self.assertEqual(result, expected_csv)

    def test_json_to_csv_output_path(self):
        json_data = [
            {"name": "John", "age": "30", "city": "New York"},
            {"name": "Jane", "age": "25", "city": "Los Angeles"},
            {"name": "Bob", "age": "40", "city": "Chicago"},
        ]
        expected_csv = "name,age,city\r\nJohn,30,New York\r\nJane,25,Los Angeles\r\nBob,40,Chicago\r\n"

        with StringIO() as output:
            json_to_csv(json_data, output_path=output.name)
            self.assertEqual(output.getvalue(), expected_csv)

if __name__ == "__main__":
    unittest.main()
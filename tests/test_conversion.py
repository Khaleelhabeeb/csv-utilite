import unittest
from io import StringIO
from typing import List, Dict, Any, Union
import os
import tempfile

def csv_to_json(csv_data: List[List[str]], orient: str = "records") -> Union[List[Dict[str, str]], Dict[str, Any]]:
    headers = csv_data[0]
    rows = csv_data[1:]

    if orient == "records":
        json_data = []
        for row in rows:
            json_data.append(dict(zip(headers, row)))
        return json_data

    elif orient == "split":
        return {
            "headers": headers,
            "values": rows
        }

    elif orient == "index":
        json_data = {}
        for i, row in enumerate(rows):
            json_data[i] = row
        return json_data

    else:
        raise ValueError(f"Invalid value for 'orient': {orient}")

def json_to_csv(json_data: Dict[Any, Any], output_path: str = None) -> List[List[str]]:
    if isinstance(json_data, dict):
        json_data = list(json_data.values())

    headers = list(json_data[0].keys())
    rows = [headers]

    for item in json_data:
        row = [str(item[header]) for header in headers]
        rows.append(row)

    if output_path:
        with open(output_path, "w", newline="") as f:
            csv_content = ",".join(headers) + "\n"
            for row in rows[1:]:
                csv_content += ",".join(row) + "\n"
            f.write(csv_content)

    return rows

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

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = os.path.join(temp_dir, "output.csv")
            json_to_csv(json_data, output_path=output_path)
            with open(output_path, "r") as f:
                result = f.read()
            self.assertEqual(result, expected_csv)

if __name__ == "__main__":
    unittest.main()
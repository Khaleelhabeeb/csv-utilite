import unittest
from unittest.mock import patch
import os

from csv_utilite.generation import generate_from_dict, generate_from_db


class TestCSVGeneration(unittest.TestCase):

    def setUp(self) -> None:
        self.test_data = [
            {'name': 'Alice', 'age': 30},
            {'name': 'Bob', 'age': 25}
        ]
        self.test_output_path = 'test_output.csv'

    def tearDown(self) -> None:
        if os.path.exists(self.test_output_path):
            os.remove(self.test_output_path)

    def test_generate_from_dict_single_dict(self):
        generate_from_dict({'name': 'Alice', 'age': 30}, self.test_output_path)
        with open(self.test_output_path, 'r') as file:
            content = file.read()
        self.assertEqual(content, 'name,age\nAlice,30\n')

    def test_generate_from_dict_list_of_dicts(self):
        generate_from_dict(self.test_data, self.test_output_path)
        with open(self.test_output_path, 'r') as file:
            content = file.read()
        self.assertEqual(content, 'name,age\nAlice,30\nBob,25\n')

    def test_generate_from_dict_custom_headers(self):
        headers = ['First Name', 'Years']
        generate_from_dict(self.test_data, self.test_output_path, headers=headers)
        with open(self.test_output_path, 'r') as file:
            content = file.read()
        self.assertEqual(content, 'First Name,Years\nAlice,30\nBob,25\n')

    @patch('your_file_name.csv.writer')
    def test_generate_from_db(self, mock_writer):
        mock_cursor = mock_writer.return_value.__enter__.return_value
        mock_cursor.fetchall.return_value = [
            ('John', 40),
            ('Mary', 35)
        ]
        mock_cursor.description = [('name',), ('age',)]

        generate_from_db('SELECT * FROM users', mock_cursor, self.test_output_path)

        mock_writer.assert_called_once_with(open(self.test_output_path, 'w', newline=''))
        mock_writer.return_value.__enter__.return_value.writerow.assert_called_once_with(['name', 'age'])
        mock_writer.return_value.__enter__.return_value.writerows.assert_called_once_with([
            ['John', 40],
            ['Mary', 35]
        ])
        
if __name__ == '__main__':
    unittest.main()
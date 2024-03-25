import unittest
import os
import tempfile
from unittest.mock import patch, MagicMock
from csv_utils.generation import generate_from_dict, generate_from_db

class TestGenerationModule(unittest.TestCase):
    def setUp(self):
        self.data_dict = {'Name': 'John', 'Age': 25, 'City': 'New York'}
        self.data_list = [{'Name': 'John', 'Age': 25, 'City': 'New York'},
                          {'Name': 'Jane', 'Age': 30, 'City': 'London'}]
        self.headers = ['Name', 'Age', 'City']
        self.temp_file = tempfile.NamedTemporaryFile(mode='w+', delete=False)
        self.temp_file_path = self.temp_file.name
        self.temp_file.close()

    def tearDown(self):
        if os.path.exists(self.temp_file_path):
            os.unlink(self.temp_file_path)

    def test_generate_from_dict(self):
        generate_from_dict(self.data_dict, self.temp_file_path, headers=self.headers)
        with open(self.temp_file_path, 'r') as file:
            lines = file.readlines()
        self.assertEqual(len(lines), 2)
        self.assertEqual(lines[0].strip(), ','.join(self.headers))
        self.assertEqual(lines[1].strip(), ','.join([self.data_dict[header] for header in self.headers]))

        generate_from_dict(self.data_list, self.temp_file_path)
        with open(self.temp_file_path, 'r') as file:
            lines = file.readlines()
        self.assertEqual(len(lines), 3)
        self.assertEqual(lines[0].strip(), ','.join(self.data_list[0].keys()))
        self.assertEqual(lines[1].strip(), ','.join([str(value) for value in self.data_list[0].values()]))
        self.assertEqual(lines[2].strip(), ','.join([str(value) for value in self.data_list[1].values()]))

        with self.assertRaises(ValueError):
            generate_from_dict([1, 2, 3], self.temp_file_path)

    @patch('csv_utils.generation.csv')
    def test_generate_from_db(self, mock_csv):
        mock_cursor = MagicMock()
        mock_cursor.description = [('Name',), ('Age',), ('City',)]
        mock_cursor.fetchall.return_value = [('John', 25, 'New York'), ('Jane', 30, 'London')]
        mock_db_connection = MagicMock()
        mock_db_connection.cursor.return_value = mock_cursor

        generate_from_db("SELECT name, age, city FROM users", mock_db_connection, self.temp_file_path)
        mock_csv.writer.return_value.writerow.assert_any_call(['Name', 'Age', 'City'])
        mock_csv.writer.return_value.writerows.assert_called_with([('John', 25, 'New York'), ('Jane', 30, 'London')])

        with self.assertRaises(ValueError):
            generate_from_db("INVALID QUERY", mock_db_connection, self.temp_file_path)

if __name__ == '__main__':
    unittest.main()
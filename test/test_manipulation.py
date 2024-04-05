import unittest
import csv
from unittest.mock import patch, MagicMock
from typing import Iterable, Any, Callable, List, Dict, Optional
from csv_utilities.manipulation import filter_rows, sort_rows, merge_files 

class CSVUtilsTest(unittest.TestCase):

    def test_filter_rows(self):
        rows = [[1, 'a'], [2, 'b'], [3, 'a']]
        filtered = filter_rows(rows, lambda row: row[1] == 'a')
        self.assertEqual(filtered, [[1, 'a'], [3, 'a']])

    def test_sort_rows(self):
        rows = [[2, 'b'], [1, 'a'], [3, 'a']]
        sorted_rows = sort_rows(rows, key=lambda row: row[0])
        self.assertEqual(sorted_rows, [[1, 'a'], [2, 'b'], [3, 'a']])

    def test_merge_files_with_same_headers(self):
        with patch('csv.reader') as mock_reader:
            mock_reader.side_effect = [[['A', 'B'], [1, 'x']], [['A', 'B'], [2, 'y']]]
            merge_files(['file1.csv', 'file2.csv'], 'output.csv')

            # Assert that rows are merged and written correctly
            mock_writer = MagicMock()
            mock_writer.writerow.assert_called_once_with(['A', 'B'])
            mock_writer.writerows.assert_called_once_with([[1, 'x'], [2, 'y']])

    def test_merge_files_with_different_headers_and_custom_header(self):
        with patch('csv.reader') as mock_reader:
            mock_reader.side_effect = [[['X', 'Y'], [1, 'x']], [['A', 'B'], [2, 'y']]]
            merge_files(['file1.csv', 'file2.csv'], 'output.csv', header=['C', 'D'])

            # Assert that custom header is used
            mock_writer = MagicMock()
            mock_writer.writerow.assert_called_once_with(['C', 'D'])

    def test_merge_files_with_different_headers_and_error(self):
        with patch('csv.reader') as mock_reader:
            mock_reader.side_effect = [[['X', 'Y'], [1, 'x']], [['A', 'B'], [2, 'y']]]
            with self.assertRaises(ValueError):  # Assert that ValueError is raised
                merge_files(['file1.csv', 'file2.csv'], 'output.csv')

if __name__ == '__main__':
    unittest.main()
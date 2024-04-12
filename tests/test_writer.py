import unittest
from unittest.mock import patch, MagicMock
import csv
from typing import Iterable, Any, Union, Optional
from csv_utilite.writer import Writer


class Writer(Writer):
    """
    A CSV writer class that extends the functionality of the built-in csv.writer.

    This class provides additional features such as automatic type casting,
    handling missing values, and support for different dialects.
    """

    def __init__(self, file_or_writer, dialect='excel', na_rep=None):
        """
        Initialize a Writer instance.

        Args:
            file_or_writer (str, path-like, or writer object): A file path, URL, or a writer object
                                                                to write the CSV data to.
            dialect (str, optional): The dialect to use for writing the CSV file.
                                       Default is 'excel'.
            na_rep (str, optional): A string representing the value to use for missing or null values.
                                       Default is an empty string.
        """
        if isinstance(file_or_writer, str):
            self._writer = csv.writer(open(file_or_writer, 'w', newline=''), dialect=dialect)
        else:
            self._writer = csv.writer(file_or_writer, dialect=dialect)
        self.na_rep = na_rep or ''

    def writerow(self, row: Iterable[Any]):
        """
        Write a row of data to the CSV file.

        Args:
            row (Iterable[Any]): An iterable containing the values for the row.
        """
        self._writer.writerow([self._format_value(value) for value in row])

    def writerows(self, rows: Iterable[Iterable[Any]]):
        """
        Write multiple rows of data to the CSV file.

        Args:
            rows (Iterable[Iterable[Any]]): An iterable of iterables containing the values for each row.
        """
        self._writer.writerows([[self._format_value(value) for value in row] for row in rows])

    def _format_value(self, value: Any) -> Optional[str]:
        """
        Format a value for writing to the CSV file.

        Args:
            value (Any): The value to be formatted.

        Returns:
            Optional[str]: The formatted value as a string, or None if the value represents a missing or null value.
        """
        if value is None:
            return self.na_rep
        elif isinstance(value, bool):
            return str(value).lower()
        else:
            return str(value)

class WriterTest(unittest.TestCase):

    @patch('csv.writer')
    def test_writerow_with_string_values(self, mock_writer):
        # Mock the csv.writer to verify output
        mock_writer.return_value = MagicMock()
        writer = Writer('data.csv')
        writer.writerow(['apple', 'banana', 10])

        # Assert that the mock writer is called with the expected data
        mock_writer.return_value.writerow.assert_called_once_with(['apple', 'banana', '10'])

    @patch('csv.writer')
    def test_writerow_with_mixed_types(self, mock_writer):
        # Mock the csv.writer to verify output
        mock_writer.return_value = MagicMock()
        writer = Writer('data.csv')
        writer.writerow([True, None, 3.14])

        # Assert that the mock writer is called with formatted data
        mock_writer.return_value.writerow.assert_called_once_with(['true', '', '3.14'])

    @patch('csv.writer')
    def test_writerows_with_multiple_rows(self, mock_writer):
        # Mock the csv.writer to verify output
        mock_writer.return_value = MagicMock()
        writer = Writer('data.csv')
        rows = [['x', 'y'], ['a', 1]]
        writer.writerows(rows)

        # Assert that the mock writer is called with formatted rows
        mock_writer.return_value.writerows.assert_called_once_with([['x', 'y'], ['a', '1']])
        
if __name__ == '__main__':
    unittest.main()

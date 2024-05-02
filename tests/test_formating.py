import unittest
from unittest.mock import patch
from typing import Iterable, Any, List, Optional
import csv
from csv_utilite.formating import quote_fields, remove_quotes, handle_newlines

def quote_fields(data: Iterable[Iterable[Any]], quoting: Optional[int] = csv.QUOTE_MINIMAL) -> List[List[str]]:
    quoted_rows = []
    for row in data:
        quoted_row = []
        for field in row:
            if quoting == csv.QUOTE_ALL:
                quoted_field = csv.writer([], quoting=quoting).writerow([field])[0]
            elif quoting == csv.QUOTE_NONNUMERIC:
                try:
                    float(field)
                    quoted_field = str(field)
                except ValueError:
                    quoted_field = csv.writer([], quoting=quoting).writerow([field])[0]
            elif quoting == csv.QUOTE_NONE:
                quoted_field = str(field)
            else:
                quoted_field = csv.writer([], quoting=quoting).writerow([field])[0]
            quoted_row.append(quoted_field)
        quoted_rows.append(quoted_row)
    return quoted_rows

def remove_quotes(data: Iterable[Iterable[str]]) -> List[List[str]]:
    unquoted_rows = []
    for row in data:
        unquoted_row = []
        for field in row:
            unquoted_field = field.strip('"')
            unquoted_row.append(unquoted_field)
        unquoted_rows.append(unquoted_row)
    return unquoted_rows

def handle_newlines(data: Iterable[Iterable[str]], replacement: str = '\\n') -> List[List[str]]:
    formatted_rows = []
    for row in data:
        formatted_row = []
        for field in row:
            formatted_field = field.replace('\n', replacement)
            formatted_row.append(formatted_field)
        formatted_rows.append(formatted_row)
    return formatted_rows

class CSVUtilsTest(unittest.TestCase):
    def test_quote_fields_all(self):
        data = [['apple', 'banana,split'], [1, 2.5]]
        quoted_rows = quote_fields(data, csv.QUOTE_ALL)
        self.assertEqual(quoted_rows, [['"apple"', '"banana,split"'], ['"1"', '"2.5"']])

    def test_quote_fields_nonnumeric(self):
        data = [['apple', 'banana'], [1, 2.5]]
        quoted_rows = quote_fields(data, csv.QUOTE_NONNUMERIC)
        self.assertEqual(quoted_rows, [['"apple"', '"banana"'], ['1', '"2.5"']])

    def test_quote_fields_minimal(self):
        data = [['apple', 'banana,split'], [1, 2.5]]
        quoted_rows = quote_fields(data)  # Default minimal quoting
        self.assertEqual(quoted_rows, [['apple', '"banana,split"'], ['1', '2.5']])

    def test_quote_fields_none(self):
        data = [['apple', 'banana,split'], [1, 2.5]]
        quoted_rows = quote_fields(data, csv.QUOTE_NONE)
        self.assertEqual(quoted_rows, [['apple', 'banana,split'], ['1', '2.5']])

    def test_remove_quotes(self):
        data = [['"apple"', '"banana,split"'], ['"1"', '"2.5"']]
        unquoted_rows = remove_quotes(data)
        self.assertEqual(unquoted_rows, [['apple', 'banana,split'], ['1', '2.5']])

    def test_handle_newlines(self):
        data = [['field\nwith\nnewline'], ['another']]
        formatted_rows = handle_newlines(data)
        self.assertEqual(formatted_rows, [['field\\nwith\\nnewline'], ['another']])

    def test_handle_newlines_custom_replacement(self):
        data = [['field\nwith\nnewline'], ['another']]
        formatted_rows = handle_newlines(data, replacement='<br>')
        self.assertEqual(formatted_rows, [['field<br>with<br>newline'], ['another']])

if __name__ == '__main__':
    unittest.main()
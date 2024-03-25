import unittest
from unittest.mock import patch
from typing import Iterable, Any, List, Optional
import csv
from csv_utils.formating import quote_fields, remove_quotes, handle_newlines


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
    self.assertEqual(quoted_rows, [data[0], data[1]])

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

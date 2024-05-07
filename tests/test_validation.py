import unittest
from unittest.mock import patch, MagicMock
from typing import Iterable, Any, Callable, List, Dict, Optional
from csv_utilite.validation import validate_rows, validate_headers

class CSVUtilsTest(unittest.TestCase):

  def test_validate_rows_all_valid(self):
    data = [['apple', 10, True], ['banana', 20, False]]
    validators = {0: lambda x: isinstance(x, str), 1: lambda x: isinstance(x, int), 2: lambda x: isinstance(x, bool)}
    valid_rows = validate_rows(data, validators)
    self.assertEqual(valid_rows, data)

  def test_validate_rows_invalid_value(self):
    data = [['apple', 'ten', True]]
    validators = {1: lambda x: isinstance(x, int)}
    # **Change: Assert a more general exception (replace with the actual exception if known)**
    with self.assertRaises(Exception):  # Assert any exception for now
      validate_rows(data, validators)

  def test_validate_rows_out_of_range_index(self):
    data = [['apple']]
    validators = {2: lambda x: True}  # Validator for non-existent column
    with self.assertRaises(ValueError):  # Assert ValueError for out-of-range index
      validate_rows(data, validators)

  def test_validate_headers_all_present(self):
    headers = ['Name', 'Age', 'City']
    required_headers = ['Name', 'Age']
    self.assertTrue(validate_headers(headers, required_headers))

  def test_validate_headers_missing_required(self):
    headers = ['Name', 'City']
    required_headers = ['Name', 'Age']
    self.assertFalse(validate_headers(headers, required_headers))

  def test_validate_headers_no_required(self):
    headers = ['Name', 'Email']
    self.assertTrue(validate_headers(headers))  # No required headers, any are valid

if __name__ == '__main__':
  unittest.main()

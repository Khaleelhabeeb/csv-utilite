import csv
from typing import Iterable, Any, List, Optional

def quote_fields(rows: Iterable[Iterable[Any]], quoting: Optional[int] = csv.QUOTE_MINIMAL) -> List[List[str]]:
  """
  Quote fields in CSV rows based on the specified quoting mode.

  Args:
      rows (Iterable[Iterable[Any]]): An iterable of iterables containing the CSV data rows.
      quoting (Optional[int]): The quoting mode to use. Default is csv.QUOTE_MINIMAL.
          Possible values are:
          - csv.QUOTE_ALL: Quote all fields.
          - csv.QUOTE_MINIMAL: Quote fields only if necessary (default).
          - csv.QUOTE_NONNUMERIC: Quote all non-numeric fields.
          - csv.QUOTE_NONE: Never quote fields.

  Returns:
      List[List[str]]: A list of lists containing the quoted rows.
  """
  quoted_rows = []
  for row in rows:
      quoted_row = []
      for value in row:
          if quoting == csv.QUOTE_ALL or (quoting == csv.QUOTE_NONNUMERIC and not isinstance(value, (int, float))):
              quoted_row.append('"' + str(value) + '"')  # Use double quotes directly
          elif quoting == csv.QUOTE_MINIMAL and (isinstance(value, str) and (',' in value or '\n' in value)):
              quoted_row.append('"' + value + '"')
          else:
              quoted_row.append(str(value))
      quoted_rows.append(quoted_row)
  return quoted_rows

def remove_quotes(rows: Iterable[Iterable[Any]]) -> List[List[str]]:
  """
  Remove quotes from fields in CSV rows.

  Args:
      rows (Iterable[Iterable[Any]]): An iterable of iterables containing the CSV data rows.

  Returns:
      List[List[str]]: A list of lists containing the rows with quotes removed.
  """
  unquoted_rows = []
  for row in rows:
      unquoted_row = [str(value).strip('"') for value in row]
      unquoted_rows.append(unquoted_row)
  return unquoted_rows

def handle_newlines(rows: Iterable[Iterable[Any]], replacement: str = '\\n') -> List[List[str]]:
  """
  Replace newline characters within fields in CSV rows with a specified replacement string.

  Args:
      rows (Iterable[Iterable[Any]]): An iterable of iterables containing the CSV data rows.
      replacement (str): The string to replace newline characters with. Default is '\\n'.

  Returns:
      List[List[str]]: A list of lists containing the rows with newline characters replaced.
  """
  formatted_rows = []
  for row in rows:
      formatted_row = [str(value).replace('\n', replacement) for value in row]
      formatted_rows.append(formatted_row)
  return formatted_rows
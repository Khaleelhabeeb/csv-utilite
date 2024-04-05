import csv
from typing import Iterable, Any, Callable, List, Dict, Optional

def validate_rows(rows: Iterable[Iterable[Any]], validators: Dict[int, Callable[[Any], bool]]) -> List[List[Any]]:
    """
    Validate rows in a CSV data based on a dictionary of validators.

    Args:
        rows (Iterable[Iterable[Any]]): An iterable of iterables containing the CSV data rows.
        validators (Dict[int, Callable[[Any], bool]]): A dictionary mapping column indexes to validator functions.
            The validator functions should take a value as input and return True if the value is valid, False otherwise.

    Returns:
        List[List[Any]]: A list of lists containing the valid rows.

    Raises:
        ValueError: If any row contains an invalid value based on the provided validators.
    """
    valid_rows = []
    for row in rows:
        is_valid = True
        for col_index, validator in validators.items():
            if col_index >= len(row):
                raise ValueError(f"Column index {col_index} is out of range for row: {row}")
            value = row[col_index]
            if not validator(value):
                is_valid = False
                break
        if is_valid:
            valid_rows.append(row)
    return valid_rows

def validate_headers(headers: Iterable[Any], required_headers: Optional[List[str]] = None) -> bool:
    """
    Validate CSV headers against a list of required headers.

    Args:
        headers (Iterable[Any]): An iterable containing the CSV headers.
        required_headers (Optional[List[str]]): A list of required headers. If not provided, any headers are considered valid.

    Returns:
        bool: True if the headers are valid, False otherwise.
    """
    if required_headers is None:
        return True

    headers_set = set(headers)
    required_headers_set = set(required_headers)
    return required_headers_set.issubset(headers_set)
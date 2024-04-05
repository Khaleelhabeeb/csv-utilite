import csv
from typing import Iterable, Any, Callable, List, Dict, Optional

def filter_rows(rows: Iterable[Iterable[Any]], filter_func: Callable[[Iterable[Any]], bool]) -> List[List[Any]]:
    """
    Filter rows in a CSV data based on a given condition.

    Args:
        rows (Iterable[Iterable[Any]]): An iterable of iterables containing the CSV data rows.
        filter_func (Callable[[Iterable[Any]], bool]): A function that takes a row as input and returns True
            if the row should be included, False otherwise.

    Returns:
        List[List[Any]]: A list of lists containing the filtered rows.
    """
    return [row for row in rows if filter_func(row)]

def sort_rows(rows: Iterable[Iterable[Any]], key: Optional[Callable[[Iterable[Any]], Any]] = None, reverse: bool = False) -> List[List[Any]]:
    """
    Sort rows in a CSV data based on a given key function.

    Args:
        rows (Iterable[Iterable[Any]]): An iterable of iterables containing the CSV data rows.
        key (Optional[Callable[[Iterable[Any]], Any]]): A function that takes a row as input and returns
            the value to sort by. If not provided, the rows will be sorted based on their original order.
        reverse (bool): If True, the rows will be sorted in descending order.

    Returns:
        List[List[Any]]: A list of lists containing the sorted rows.
    """
    return sorted(rows, key=key, reverse=reverse)

def merge_files(file_paths: List[str], output_path: str, dialect: str = 'excel', has_header: bool = True, header: Optional[List[str]] = None):
    """
    Merge multiple CSV files into a single output file.

    Args:
        file_paths (List[str]): A list of file paths for the input CSV files.
        output_path (str): The file path for the output CSV file.
        dialect (str): The dialect to use for parsing and writing the CSV files.
        has_header (bool): Whether the input CSV files have a header row.
        header (Optional[List[str]]): A custom header to use for the output file.
            If not provided, the header from the first input file will be used.

    Raises:
        ValueError: If the input files have different headers and no custom header is provided.
    """
    headers = []
    rows = []

    for file_path in file_paths:
        with open(file_path, 'r') as file:
            reader = csv.reader(file, dialect=dialect)
            if has_header:
                header = next(reader)
                if headers and header != headers[0]:
                    if not header:
                        raise ValueError("Input files have different headers, and no custom header is provided.")
                headers.append(header)
            rows.extend(reader)

    if header is None:
        header = headers[0] if headers else []

    with open(output_path, 'w', newline='') as file:
        writer = csv.writer(file, dialect=dialect)
        if header:
            writer.writerow(header)
        writer.writerows(rows)
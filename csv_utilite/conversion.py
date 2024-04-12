import csv
import json
from typing import Iterable, Any, Union, List, Dict, Optional

def csv_to_json(rows: Iterable[Iterable[Any]], headers: Optional[List[str]] = None, orient: str = 'records') -> Union[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Convert CSV data to JSON format.

    Args:
        rows (Iterable[Iterable[Any]]): An iterable of iterables containing the CSV data rows.
        headers (Optional[List[str]]): An optional list containing the CSV headers.
                                       If not provided, the first row will be used as headers.
        orient (str): The JSON orientation. Possible values are 'records' (default), 'split', 'index', 'columns', 'values'.

    Returns:
        Union[List[Dict[str, Any]], Dict[str, Any]]: The JSON data, either as a list of dictionaries (for 'records' orientation)
                                                    or a dictionary with nested data (for other orientations).

    Raises:
        ValueError: If the 'orient' value is invalid or there's an issue with the CSV data.
    """

    data = list(rows)
    if not data:
        raise ValueError("Empty CSV data provided")

    if headers is None:
        headers = data.pop(0) if len(data) > 0 else []
        # Check data type of headers (should be strings)

    if orient == 'records':
        return [dict(zip(headers, row)) for row in data]
    elif orient == 'split':
        return dict(zip(['headers', 'values'], [headers, data]))
    elif orient == 'index':
        return {idx: row for idx, row in enumerate(data)}
    elif orient == 'columns':
        return {header: [row[idx] for row in data] for idx, header in enumerate(headers)}
    elif orient == 'values':
        return data
    else:
        raise ValueError(f"Invalid 'orient' value: {orient}")

def json_to_csv(data: Union[List[Dict[str, Any]], Dict[str, Any]], headers: Optional[List[str]] = None, output_path: Optional[str] = None) -> List[List[Any]]:
    """
    Convert JSON data to CSV format.

    Args:
        data (Union[List[Dict[str, Any]], Dict[str, Any]]): The JSON data, either as a list of dictionaries
                                                            or a dictionary with nested data.
        headers (Optional[List[str]]): An optional list containing the desired CSV headers.
                                       If not provided, the keys from the first dictionary in the JSON data will be used.
        output_path (Optional[str]): The file path to write the CSV data to. If not provided, the data will be returned as a list of lists.

    Returns:
        List[List[Any]]: The CSV data as a list of lists, unless an output_path is provided.
    """

    if isinstance(data, list):
        if headers is None:
            headers = list(data[0].keys()) if data else []
        rows = [list(row.values()) for row in data]
    else:
        if headers is None:
            headers = list(data.values())[0].keys()
        rows = [[row[header] for header in headers] for row in list(data.values())]

    if output_path:
        with open(output_path, 'w', newline='') as file:
            writer = csv.writer(file)
            if headers:
                writer.writerow(headers)
            writer.writerows(rows)
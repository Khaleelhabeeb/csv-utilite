import csv
from typing import Iterator, Optional, Any, Union, List, Dict

class Reader:
    """
    A CSV reader class that extends the functionality of the built-in csv.reader.

    This class provides additional features such as automatic type casting,
    handling missing values, and support for different dialects.
    """

    def __init__(self, file_or_iterator, dialect='excel', type_cast=True, na_values=None):
        """
        Initialize a Reader instance.

        Args:
            file_or_iterator (str, path-like, or iterator): A file path, URL, or an iterator
                to read the CSV data from.
            dialect (str, optional): The dialect to use for parsing the CSV file.
                Default is 'excel'.
            type_cast (bool, optional): Whether to automatically cast data types.
                Default is True.
            na_values (str or list, optional): A string or list of strings representing
                missing or null values in the CSV data.
        """
        self._reader = csv.reader(file_or_iterator, dialect=dialect)
        self.type_cast = type_cast
        self.na_values = na_values or ['']

    def __iter__(self):
        return self

    def __next__(self) -> List[Any]:
        """
        Return the next row from the CSV file as a list.

        If type_cast is True, the values will be automatically cast to their
        corresponding data types (int, float, bool, etc.). Missing or null values
        will be represented as None.

        Returns:
            list: A list containing the values of the next row.
        """
        row = next(self._reader)

        if self.type_cast:
            row = [self._cast_value(value) for value in row]

        return row

    def _cast_value(self, value: str) -> Optional[Union[int, float, bool]]:
        """
        Cast a string value to its corresponding data type.

        Args:
            value (str): The string value to be cast.

        Returns:
            Optional[Union[int, float, bool]]: The casted value, or None if the
            value represents a missing or null value.
        """
        if value in self.na_values:
            return None

        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                if value.lower() in ('true', 't'):
                    return True
                elif value.lower() in ('false', 'f'):
                    return False
                else:
                    return value
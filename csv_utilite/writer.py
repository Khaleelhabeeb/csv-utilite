import csv
from typing import Iterable, Any, Union, Optional, IO

class Writer:
    """
    A CSV writer class that extends the functionality of the built-in csv.writer.

    This class provides additional features such as automatic type casting,
    handling missing values, and support for different dialects.
    """

    def __init__(self, file_or_writer: Union[str, IO[str]], dialect='excel', na_rep: str = ''):
        """
        Initialize a Writer instance.

        Args:
            file_or_writer (str, path-like object, or writer object): A file path, URL, or a writer object
                                                                      to write the CSV data to.
            dialect (str, optional): The dialect to use for writing the CSV file.
                                       Default is 'excel'.
            na_rep (str, optional): A string representing the value to use for missing or null values.
                                       Default is an empty string.

        Raises:
            ValueError: If file_or_writer is not a string, path-like object, or a writer object.
        """
        if not isinstance(file_or_writer, (str, IO[str])):
            raise ValueError("file_or_writer must be a string, path-like object, or a writer object")

        if isinstance(file_or_writer, str):
            self._writer = csv.writer(open(file_or_writer, 'w', newline=''), dialect=dialect)
        else:
            self._writer = csv.writer(file_or_writer, dialect=dialect)
        self.na_rep = na_rep

    def writerow(self, row: Iterable[Any]) -> None:
        """
        Write a row of data to the CSV file.

        Args:
            row (Iterable[Any]): An iterable containing the values for the row.

        Raises:
            ValueError: If the row is empty.
        """
        if not row:
            raise ValueError("Cannot write empty row")
        self._writer.writerow([self._format_value(value) for value in row])

    def writerows(self, rows: Iterable[Iterable[Any]]) -> None:
        """
        Write multiple rows of data to the CSV file.

        Args:
            rows (Iterable[Iterable[Any]]): An iterable of iterables containing the values for each row.

        Raises:
            ValueError: If any row is empty.
        """
        for row in rows:
            if not row:
                raise ValueError("Cannot write empty row")
        self._writer.writerows([[self._format_value(value) for value in row] for row in rows])

    def set_na_rep(self, na_rep: str) -> None:
        """
        Set the value to be used for missing or null values.

        Args:
            na_rep (str): The new value to be used for missing or null values.
        """
        self.na_rep = na_rep

    def _format_value(self, value: Any) -> Union[str, None]:
        """
        Format a value for writing to the CSV file.

        Args:
            value (Any): The value to be formatted.

        Returns:
            Union[str, None]: The formatted value as a string, or None if the value represents a missing or null value.
        """
        if value is None:
            return self.na_rep

import os

class CSVLogger:
    """
    used to create and write .csv files 
    """

    def __init__(self, columns: list[str], prefix: str = "log"):
        """
        columns - each data column name
        prefix - the file name prefix (e.g. 'test' for tests or 'flight' for flight data)
        """
        self._filename = self._next_filename(prefix)
        self._write_header(columns)

    # --------------- PUBLIC METHODS --------------- #

    @property
    def filename(self) -> str:
        return self._filename

    def append(self, row: list) -> None:
        """appends a single row to the .csv"""
        
        with open(self._filename, 'a') as file:
            file.write(",".join(map(str, row)) + "\n")

    # --------------- PRIVATE HELPERS --------------- #

    @staticmethod
    def _next_filename(prefix: str) -> str:
        """
        gets the new file name and number (prevents duplicate files)
        """
        existing = os.listdir()
        index = 1
        while f"{prefix}{index}.csv" in existing:
            index += 1
        return f"{prefix}{index}.csv"

    def _write_header(self, columns: list[str]) -> None:
        with open(self._filename, 'w') as f:
            f.write(",".join(columns) + "\n")
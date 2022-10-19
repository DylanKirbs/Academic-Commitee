# Manager Class for the Hemis Database (JSON)

# Imports
import json

# Class


class HemisDBManager:
    def __init__(self, path: str) -> None:
        """
        Loads DB from path on INIT"""
        self._data = None
        self._path = path

        self.load()

    def load(self) -> dict:
        """
        Load the data from the DB

        :Return: The dictionary of the DB
        """
        with open(self._path, "r") as f:
            self._data = json.load(f)

        return self._data

    def save(self):
        """
        Save the data from the Manager into the DB
        """
        with open(self._path, "w") as f:
            json.dump(self._data, f)

    def addDegree(self, degree: dict):
        """
        Takes in a degree dict as follows:
        key: abbreviation
        value: name

        Eg. {"bsc": "Bachelor of Science"}

        Note: This will be added to the DB or updated if it already exists
        """

        # make the keys lower case
        degree = {key.lower(): val for key, val in degree.items()}

        self._data["Degrees"].update(degree)


    @property
    def data(self) -> dict:
        """
        Note: This give you direct access to the data
        """
        return self._data

    @property
    def calenderURL(self) -> str:
        """
        Returns the URL string
        """
        return self._data["URL"]

    @property
    def faculties(self) -> list[str]:
        """
        Returns the list of faculties
        """
        return self._data["Faculties"]

    @property
    def degrees(self) -> list[dict]:
        """
        Returns the list of degrees
        """
        return self._data["Degrees"]

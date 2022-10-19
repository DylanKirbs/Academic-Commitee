from pprint import pprint
from PyPDF2 import PdfReader
from Utils import *
import json

class SunYearbook:
    """
    Class to simplify the SUN yearbook download process
    """

    def __init__(self, url, path, faculty):
        self.url = url
        self.faculty = faculty
        self.filename = os.path.join(path, faculty + ".pdf")

    def fileExists(self):
        """
        Checks if the file exists

        :return: True if the file exists, False otherwise
        """

        return os.path.isfile(self.filename)

    def download(self):
        """
        Downloads the yearbook for the given faculty
        """

        downloadFile(self._buildDownloadUrl(), self.filename, 1024)

    def _buildDownloadUrl(self):
        """
        Builds the download url for the given faculty
        :return: The download url
        """

        return self.url + self.faculty + ".pdf"

    def getOutline(self):
        """
        Gets the outline of the yearbook as a nested list of titles

        :return: The outline of the yearbook
        """

        pdf = PdfReader(self.filename)

        outlines = pdf.getOutlines()

        return self._parseOutline(outlines)

    def _parseOutline(self, outline):
        """
        Parses the outline of the yearbook into a dictionary or destinations and page numbers

        :param outline: The outline of the yearbook
        :return: The parsed outline
        """

        parsed_outline = []

        for item in outline:
            if isinstance(item, list):
                parsed_outline.append(self._parseOutline(item))
            else:
                parsed_outline.append(item.title)

        return parsed_outline
        

# Tester
if __name__ == "__main__":


    from HemisDBManager import HemisDBManager
    HemisDB = HemisDBManager("HemisDB.json")

    yearBookPath = os.path.join(os.getcwd(), "Yearbooks")
    outlinePath = os.path.join(os.getcwd(), "Outlines")

    pprint(HemisDB.degrees)

    HemisDB.save()


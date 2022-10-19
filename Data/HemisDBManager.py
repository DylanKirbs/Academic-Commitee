from dataclasses import dataclass
from os import path
from shutil import copyfile
import sqlite3

@dataclass
class faculty:
    name: str

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self) -> str:
        return f"{self.name}"

@dataclass
class module:
    name: str
    code: str
    credits: faculty

    def __str__(self) -> str:
        return f"{self.name} ({self.code})"

    def __repr__(self) -> str:
        return f"{self.name} ({self.code})"

@dataclass
class degree:
    abbreviation: str
    name: str
    faculty: faculty
    modules: list[module]

    def __str__(self) -> str:
        return f"{self.name} ({self.abbreviation})"

    def __repr__(self) -> str:
        return f"{self.name} ({self.abbreviation})"

class HemisDataBase():

    def __init__(self):
        # Connect to the database
        self._conn = sqlite3.connect('Data/HemisDB.db')
        self._c = self._conn.cursor()

        self._initTables()   

    def _initTables(self):
        """ Initialise the tables with the default values if the tables do not exist
        :return: None
        """
        # Create the tables if it doesn't exist
        # The faculties
        faculty_table = """CREATE TABLE IF NOT EXISTS faculty (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        ); """

        # The modules
        module_table = """CREATE TABLE IF NOT EXISTS module (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            code INTEGER NOT NULL,
            credits INTEGER NOT NULL
        ); """

        # The degrees
        degree_table = """CREATE TABLE IF NOT EXISTS degree (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            abbreviation TEXT NOT NULL,
            name TEXT NOT NULL,
            faculty_id INTEGER NOT NULL,
            module_ids TEXT NOT NULL,
            FOREIGN KEY (faculty_id) REFERENCES faculty(id)
        ); """

        self.executeSQL(faculty_table)
        self.executeSQL(module_table)
        self.executeSQL(degree_table)
        self.commitSQL()

    def executeSQL(self, sql):
        """ Execute the SQL statement
        :param sql: The SQL statement
        :return: None

        NOTE: This is a wrapper for the cursor execute method
        WARNING: This does not commit the changes to the database
        """
        self._c.execute(sql)

    def commitSQL(self):
        """ Commit the changes to the database
        :return: None

        NOTE: This is a wrapper for the connection commit method
        WARNING: This method is not preferred as it is not managed by the API
        """
        self._conn.commit()

    def backupDB(self):
        """ Backup the database to the backup folder
        :return: None
        """
        
        copyfile('Data/HemisDB.db', 'Data/Backup/HemisDB.db')

    def restoreDB(self):
        """ Restore the database from the backup folder
        :return: None
        """
        if not path.exists('Data/Backup/HemisDB.db'):
            raise Exception('Backup database does not exist')

        copyfile('Data/Backup/HemisDB.db', 'Data/HemisDB.db')

    def closeDB(self):
        """ Close the database connection
        :return: None
        """
        self._conn.close()

    def addFaculty(self, faculty: faculty):
        """ Add a faculty to the database
        :param faculty: The faculty to add
        :return: None
        """
        sql = f"INSERT INTO faculty (name) VALUES ('{faculty.name}');"
        self.executeSQL(sql)
        self.commitSQL()

    def addModule(self, module: module):
        """ Add a module to the database
        :param module: The module to add
        :return: None
        """
        sql = f"INSERT INTO module (name, code, credits) VALUES ('{module.name}', '{module.code}', '{module.credits}');"
        self.executeSQL(sql)
        self.commitSQL()

    def addDegree(self, degree: degree):
        """ Add a degree to the database
        :param degree: The degree to add
        :return: None
        """
        # Get the faculty id
        sql = f"SELECT id FROM faculty WHERE name = '{degree.faculty.name}';"
        self.executeSQL(sql)
        faculty_id = self._c.fetchone()[0]

        # Get the module ids
        module_ids = []
        for module in degree.modules:
            sql = f"SELECT id FROM module WHERE name = '{module.name}' AND code = '{module.code}';"
            self.executeSQL(sql)
            module_ids.append(self._c.fetchone()[0])

        sql = f"INSERT INTO degree (abbreviation, name, faculty_id, module_ids) VALUES ('{degree.abbreviation}', '{degree.name}', '{faculty_id}', '{module_ids}');"
        self.executeSQL(sql)
        self.commitSQL()

    def getFaculties(self):
        """ Get all the faculties from the database
        :return: A list of faculties
        """
        sql = "SELECT * FROM faculty;"
        self.executeSQL(sql)
        faculties = self._c.fetchall()
        faculties = list(faculty(f[1]) for f in faculties)
        return faculties

if __name__ == "__main__":
    # Test the database
    db = HemisDataBase()

    print(db.getFaculties())

    db.closeDB()
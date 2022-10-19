from os import path
from shutil import copyfile
import sqlite3

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
            number INTEGER NOT NULL,
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
        

if __name__ == "__main__":
    # Test the database
    db = HemisDataBase()

from pprint import pprint
import sys
from HemisDBManager import HemisDBManager


def addDegreeDialogue():
    print("Warning: This script will permanently modify the database. Continue? (y/n)")
    if input() != "y":
        sys.exit()

    HemisDB = HemisDBManager("Data/HemisDB.json")

    print("Degrees:")
    pprint(HemisDB.degrees)

    acronym = input("Enter the acronym of the degree: ")
    name = input("Enter the name of the degree: ")

    print("Confirm you with to add '{acronym}': '{name}' to the HemisDB.json file? (y/n)".format(acronym=acronym, name=name))
    if input() != "y":
        sys.exit()

    HemisDB.addDegree({acronym: name})
    HemisDB.save()
    print("Degree added successfully")

def removeDegreeDialogue():
    print("Warning: This script will permanently modify the database. Continue? (y/n)")
    if input() != "y":
        sys.exit()

    HemisDB = HemisDBManager("Data/HemisDB.json")

    print("Degrees:")
    pprint(HemisDB.degrees)

    acronym = input("Enter the acronym of the degree: ")

    print("Confirm you with to remove '{acronym}' from the HemisDB.json file? (y/n)".format(acronym=acronym))
    if input() != "y":
        sys.exit()

    HemisDB.removeDegree(acronym)
    HemisDB.save()
    print("Degree removed successfully")

if __name__ == "__main__":

    print("----- HemisDB Modifier -----")

    choice = ""

    while choice != "x":

        print("v: View degrees")
        print("a: Add Degree")
        print("r: Remove Degree")
        print("x: Exit")
        choice = input("Enter your choice: ")

        if choice == "v":
            HemisDB = HemisDBManager("Data/HemisDB.json")
            pprint(HemisDB.degrees)
        elif choice == "a":
            addDegreeDialogue()
        elif choice == "r":
            removeDegreeDialogue()
        else:
            print("Invalid command")

        print("")

    print("Exiting...")
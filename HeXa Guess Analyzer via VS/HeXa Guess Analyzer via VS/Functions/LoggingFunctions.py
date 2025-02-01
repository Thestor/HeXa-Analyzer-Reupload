
from datetime import datetime

def AddLog(id, pokemonName):

    try:
        with open("Databases\Log File.txt", "a") as fileObject:
            current_time = str(datetime.now().strftime("%H:%M:%S"))
            print(f"{id} has input the Pokemon {pokemonName} at {current_time}")
            fileObject.write(f"{id} has input the Pokemon {pokemonName} at {current_time}\n")
            print("Log file updated.")
            fileObject.close()

    except Exception as e:
        print("An error occured while updating the log file.")
        print(e)

def GetContributors():

    contributors = {}

    try:
        with open("Databases\Log File.txt") as fileObject:
            for line in fileObject:
                contributors[line[:9]] = contributors.get(line[:9], 0) + 1
            fileObject.close()
            return True, contributors

    except Exception as e:
        print("An error occured while reading the log file.")
        print(e)
        return False, None

def GetRecentContributions(no_of_records):

    try:
        with open("Databases\Log File.txt") as fileObject:
            contributions = [line for line in fileObject]
            fileObject.close()
            contributions2 = contributions[-no_of_records:]
            contributions = []
            return True, contributions2

    except Exception as e:
        print("An error occured while reading the log file.")
        print(e)
        return False, None
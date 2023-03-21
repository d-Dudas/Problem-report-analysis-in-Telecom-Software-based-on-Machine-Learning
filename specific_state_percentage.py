import sys
from pymongo import MongoClient

states = [
            "Correction Not Needed",
            "Closed",
            "Investigating",
            "New",
            "First Correction Ready For Testing",
            "First Correction Complete"
        ]

def print_state_percentage(key):

    # If the key isn't in the states list, then exit with error code 2
    if key not in states:
        print("Invalid key: {}".format(key))
        # Make a list of values which are lists
        print("States are: {}".format(states))
        sys.exit(2)

    prontos_collection = MongoClient().prontosdb.prontos_collection
    total_prontos = prontos_collection.count_documents({})
    prontos_with_state = 0

    for pronto in prontos_collection.find():
        if pronto["state"] == key:
            prontos_with_state += 1

    print("Prontos with state {}: {} %".format(key,prontos_with_state * 100 / total_prontos))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: {} <state>".format(sys.argv[0]))
        sys.exit(1)
    print_state_percentage(sys.argv[1])
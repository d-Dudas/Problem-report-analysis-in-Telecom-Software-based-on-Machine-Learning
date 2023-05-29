import sys
import json
from pymongo import MongoClient
import pymongo

def upload_prontos(data):
    database_port = 'mongodb://db:27017'
    prontos_collection = MongoClient(database_port).prontosdb.prontos_collection

    for value in data:
        try:
            rez = prontos_collection.insert_one(value)
            print("Inserted object: {}".format(rez.inserted_id))
        except pymongo.errors.DuplicateKeyError:
            print("Duplicated key error for = {}".format(value['title']))

    # Verify if there is a unique index set on 'problemReportId'
    # If it is, then exit
    for index in prontos_collection.list_indexes():
        if 'description' in index['key']:
            sys.exit(0)

    # Else, set the unique index
    prontos_collection.create_index([('description', pymongo.ASCENDING)], unique=True)



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Correct format: {} <json file>'.format(sys.argv[0]))
        sys.exit(1)
    try:
        file = open(sys.argv[1], "r")
        values = json.load(file)['values']
        upload_prontos(values)
    except FileNotFoundError:
        print("{}: File not found.".format(sys.argv[0]))
    except ValueError:
        print('{}: Decoding JSON has failed'.format(sys.argv[0]))
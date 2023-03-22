import pymongo
import json
from pymongo import MongoClient

# Make connection to the mongoDB
# If the database and collection doesn't exists,
# Both will be created
prontos_collection = MongoClient().prontosdb.prontos_collection

# After the documents were added, create a unique index, if doesn't exists
# json_file - the (absolute) path to the .json file with prontos
def upload_prontos(json_file):

    try:
        file = open(json_file, "r")
        data = json.load(file)['values']
    except FileNotFoundError:
        print("{}: File not found.".format(json_file))
    except ValueError:
        print('{}: Decoding JSON has failed'.format(json_file))

    for value in data:
        try:
            rez = prontos_collection.insert_one(value)
            print("Inserted object: {}".format(rez.inserted_id))
        except pymongo.errors.DuplicateKeyError:
            print("Duplicated key error for problemReportId = {}".format(value["problemReportId"]))

    # Verify if there is a unique index set on 'problemReportId'
    unique_index_alreadey_exists = False
    for index in prontos_collection.list_indexes():
        if 'problemReportId' in index['key']:
            unique_index_alreadey_exists = True

    # If doesn't exists, set the unique index
    if not unique_index_alreadey_exists:
        prontos_collection.create_index([('problemReportId', pymongo.ASCENDING)], unique=True)

# This function print a list of groups in charge
# or prontos resolution (it depends on key), and
# the occurence percentage for each
# key - valid values : "groupInCharge", "state", "faultAnalysisGroupInCharge"
def list_groups_and_resolutions_and_occ_percentages(key):
    
    total_prontos = prontos_collection.count_documents({})
    occ_count = {}
    
    #print('Total prontos: {}.'.format(total_prontos))
 
    # Create a dictionary with groups as keys, and number of occurences as value
    for pronto in prontos_collection.find():
        if pronto[key] in occ_count.keys():
            occ_count[pronto[key]] += 1
        else:
            occ_count[pronto[key]] = 1
    
    # Print the rezult
    for group in occ_count.keys():
        print("{} : {} %".format(group, occ_count[group] * 100 / total_prontos))

# This function search for features in prontos
# Creates a set with the features, and print them
def list_tested_features():
    # There are multiple prontos with
    # same feature, so we use a set
    # to put each pronto in it
    tested_features = set()

    for pronto in prontos_collection.find():
        tested_features.add(pronto["feature"])

    print(tested_features)


# This function shows the software with the most faulty prontos
def most_faulty_prontos():
    key = "release"
    #we use a dictionary to remember the number of all faulty prontos for each software
    releases={}
    maxvalue = 0

    for pronto in prontos_collection.find():

        #We check for all faulty prontos
        if pronto["state"]=="Correction Not Needed":
        # pronto[key] is a list: ['SBTS00']
        # isn't clear if this list could have multiple values
        # so we assume that it could have, for worst case scenario 
            for release in pronto[key]:
                if release in releases.keys():
                    releases[release] += 1
                    if(releases[release] > maxvalue): 
                        maxvalue = releases[release]
                else:
                    releases[release] = 1

    # It is possible for two different releases
    # to have the same amount of faulty prontos
    print("Release(s) with most faulty prontos:",end=' ')
    for i in releases.keys():
        if(releases[i] == maxvalue):
            print(i)

# This function calculates the occurence percentages
# for a specified (key) pronto state
# key - a pronto state
def print_state_percentage(state):

    total_prontos = prontos_collection.count_documents({})
    prontos_with_state = 0

    for pronto in prontos_collection.find():
        if pronto["state"] == state:
            prontos_with_state += 1

    print("Prontos with state {}: {} %".format(state,prontos_with_state * 100 / total_prontos))

# This function creates a list of prontos
# And sort them by key
# key - valid values: "attachedPRs", "informationrequestID"
def sort_by(key):
    
    # Make a list with with each pronto
    # identified by a dict: {problemReportId : length of the key's value's list}
    prontos_list = []
    for pronto in prontos_collection.find():
        prontos_list.append({"problemReportId" : pronto["problemReportId"], key : len(pronto[key])})

    # Sort the list by the length of the key's value's list
    prontos_list = sorted(prontos_list, key = lambda x : x[key])

    for i in prontos_list: print(i)
    #print(prontos_list)

sort_by("attachedPRs")
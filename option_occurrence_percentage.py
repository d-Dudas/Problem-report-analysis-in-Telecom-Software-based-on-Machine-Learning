import sys
from pymongo import MongoClient

valid_keys = ["groupInCharge", "state", "faultAnalysisGroupInCharge"]

def list_it(key):

    if key not in valid_keys:
        print("Invalid key: {}".format(key))
        print("Valid keys list: {}".format(valid_keys))
        sys.exit(2)
    
    prontos_collection = MongoClient().prontosdb.prontos_collection
    total_prontos = prontos_collection.count_documents({})
    occ_count = {}
    
    print('Total prontos: {}.'.format(total_prontos))
 
    # Create a dictionary with groups as keys, and number of occurences as value
    for pronto in prontos_collection.find():
        if pronto[key] in occ_count.keys():
            occ_count[pronto[key]] += 1
        else:
            occ_count[pronto[key]] = 1
    
    # Print the rezult
    for group in occ_count.keys():
        print("{} : {} %".format(group, occ_count[group] * 100 / total_prontos))

    

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: {} <option key>".format(sys.argv[0]))
        sys.exit(1)
    list_it(sys.argv[1])
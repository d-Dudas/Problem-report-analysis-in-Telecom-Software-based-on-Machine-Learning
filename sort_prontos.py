import sys
from pymongo import MongoClient

def sort_by(key):

    prontos_collection = MongoClient().prontosdb.prontos_collection

    test_instance = prontos_collection.find_one()
    # Just to avoid calling find_one() for every verification

    # If the key doesn't exists or the value of the
    # key isn't a list, then exit with error code 2
    if key not in test_instance.keys() or not isinstance(test_instance[key], list):
        print("Invalid key: {}".format(key))
        # Make a list of values which are lists
        valid_keys = []
        for pkey in test_instance.keys():
            if isinstance(test_instance[pkey], list):
                valid_keys.append(pkey)
        print("Keys are: {}".format(valid_keys))
        sys.exit(2)
    
    # Make a list with with each pronto
    # identified by a dict: {problemReportId : length of the key's value's list}
    prontos_list = []
    for pronto in prontos_collection.find():
        prontos_list.append({"problemReportId" : pronto["problemReportId"], key : len(pronto[key])})

    # Sort the list by the length of the key's value's list
    prontos_list = sorted(prontos_list, key = lambda x : x[key])

    # If the --row flag is present, then print
    # the result row by row
    if "-r" in sys.argv or "--row" in sys.argv:
        for i in prontos_list:
            print(i)
    else:
        print(prontos_list)
    

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: {} <key to sort by> <optional flag -r/--row>".format(sys.argv[0]))
        sys.exit(1)
    sort_by(sys.argv[1])
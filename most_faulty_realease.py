from pymongo import MongoClient

#connect to db
prontos_collection = MongoClient().prontosdb.prontos_collection
releases = {}
key = "release"
maxvalue = 0

for pronto in prontos_collection.find():
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
print("Release(s) with most faulty prontos:")
for i in releases.keys():
    if(releases[i] == maxvalue):
        print(i)
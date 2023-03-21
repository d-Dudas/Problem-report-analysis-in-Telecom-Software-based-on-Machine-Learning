from pymongo import MongoClient

prontos_collection = MongoClient().prontosdb.prontos_collection

# There are multiple prontos with
# same feature, so we use a set
# to put each pronto in it
tested_features = set()

for pronto in prontos_collection.find():
    tested_features.add(pronto["feature"])

print(tested_features)

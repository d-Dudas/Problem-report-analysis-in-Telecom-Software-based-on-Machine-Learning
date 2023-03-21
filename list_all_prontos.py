
from pymongo import MongoClient

prontos_collection = MongoClient().prontosdb.prontos_collection

key = "feature"
s=set()




for pronto in prontos_collection.find():
    s.add(pronto[key])

for i in s:
    print("{}.\n".format(s))
    


       


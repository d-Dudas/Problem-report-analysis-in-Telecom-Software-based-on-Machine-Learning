import nltk
from pymongo import MongoClient

database_port = 'mongodb://db:27017'

number_of_prontos_in_database = len(list(MongoClient(database_port).prontosdb.prontos_collection.find({})))

# Get each pronto's description and tokenize it
def get_tokenized_descriptions(prontos_collection = MongoClient(database_port).prontosdb.prontos_collection):
    # The tokenized descriptions are stored in the following array
    tokenized_prontos_descriptions = []
    for pronto in prontos_collection.find({}):
        tokenized_prontos_descriptions.append(nltk.word_tokenize(pronto["description"]))
    return tokenized_prontos_descriptions

def get_tokenized_title_and_description(prontos_collection = MongoClient(database_port).prontosdb.prontos_collection):
    tokenized_titles_descriptions = []
    for pronto in prontos_collection.find({}):
        aux = pronto["title"] + " " + pronto["description"]
        tokenized_titles_descriptions.append(nltk.word_tokenize(aux))
    return tokenized_titles_descriptions

def get_useful_features_list(prontos_collection = MongoClient(database_port).prontosdb.prontos_collection):
    data_list = []
    for pronto in prontos_collection.find({}):
        useful_data = {}
        useful_data["feature"] = "" if pronto["feature"] == None else pronto["feature"]
        useful_data["groupInCharge"] = "" if pronto["groupInCharge"] == None else pronto["groupInCharge"]
        useful_data["release"] = "" if pronto["release"][0] == None else pronto["release"][0]
        data_list.append(useful_data)
    return data_list

def get_gic(prontos_collection = MongoClient(database_port).prontosdb.prontos_collection):
    groupsInCharge = []
    for pronto in prontos_collection.find({}):
        groupsInCharge.append(pronto["groupInCharge"].split('_', 1)[0])
    return groupsInCharge

def get_encoded_state(prontos_collection = MongoClient(database_port).prontosdb.prontos_collection):
    state_list=[]
    for pronto in prontos_collection.find({}):
       state_list.append(pronto["state"])
    return state_list

def search_prontos_by_problemReportId_or_title(key, prontos_collection = MongoClient(database_port).prontosdb.prontos_collection):
    prontos=[]
    for pronto in prontos_collection.find({}):
        if key in pronto["problemReportId"] or key in pronto["title"]:
            prontos.append(pronto)
    return prontos

def search_pronto_by_problemReportId(problemReportId, prontos_collection = MongoClient(database_port).prontosdb.prontos_collection):
    return prontos_collection.find_one({"problemReportId": problemReportId})

def delete_pronto_by_problemReportId(problemReportId, prontos_collection = MongoClient(database_port).prontosdb.prontos_collection):
    prontos_collection.deleteOne({"problemReportId": problemReportId})
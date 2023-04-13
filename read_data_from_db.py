import nltk
from pymongo import MongoClient

# Get each pronto's description and tokenize it
def get_tokenized_descriptions(prontos_collection = MongoClient().prontosdb.prontos_collection):
    # The tokenized descriptions are stored in the following array
    tokenized_prontos_descriptions = []
    for pronto in prontos_collection.find({}):
        tokenized_prontos_descriptions.append(nltk.word_tokenize(pronto["description"]))
    
    return tokenized_prontos_descriptions

def get_tokenized_title_and_description(prontos_collection = MongoClient().prontosdb.prontos_collection):
    tokenized_titles_descriptions = []
    for pronto in prontos_collection.find({}):
        aux = pronto["title"] + " " + pronto["description"]
        tokenized_titles_descriptions.append(nltk.word_tokenize(aux))
    
    return tokenized_titles_descriptions

def get_useful_features_list(prontos_collection = MongoClient().prontosdb.prontos_collection):
    data_list = []
    for pronto in prontos_collection.find({}):
        useful_data = {}
        useful_data["feature"] = pronto["feature"]
        useful_data["groupInCharge"] = pronto["groupInCharge"]
        useful_data["release"] = pronto["release"][0]
        data_list.append(useful_data)

    return data_list

def get_gic(prontos_collection = MongoClient().prontosdb.prontos_collection):
    groupsInCharge = []
    for pronto in prontos_collection.find({}):
        groupsInCharge.append(pronto["groupInCharge"].split('_', 1)[0])
    return groupsInCharge

def get_encoded_state(prontos_collection = MongoClient().prontosdb.prontos_collection):
    state_list=[]
    for pronto in prontos_collection.find({}):
       state_list.append(pronto["state"])
    return state_list
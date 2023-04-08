from pymongo import MongoClient
import nltk
import TfidfVector
from sklearn.feature_extraction import DictVectorizer
import scipy.sparse as sp
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

def get_tokenized_title_and_description(prontos_collection = MongoClient().prontosdb.prontos_collection):
    tokenized_titles_descriptions = []
    for pronto in prontos_collection.find({}):
        aux = pronto["title"] + " " + pronto["description"]
        tokenized_titles_descriptions.append(nltk.word_tokenize(aux))
    
    return tokenized_titles_descriptions

def get_title_desc_vector():
    return TfidfVector.get_tfidfVector(
            TfidfVector.get_rejoined_processed_tokens(
                TfidfVector.get_stemmed_tokens(
                    TfidfVector.get_filtered_tokens(
                        get_tokenized_title_and_description()
                    )
                )
            )
        )

# Turn feature, groupInCharge and
# release into DictVectorizer features
def get_useful_features_dict(prontos_collection = MongoClient().prontosdb.prontos_collection):
    data_list = []
    for pronto in prontos_collection.find({}):
        useful_data = {}
        useful_data["feature"] = pronto["feature"]
        useful_data["groupInCharge"] = pronto["groupInCharge"]
        useful_data["release"] = pronto["release"][0]
        data_list.append(useful_data)

    vectorizer = DictVectorizer(sparse=True)
    useful_features = vectorizer.fit_transform(data_list)
    return useful_features

# Return the concatenated features
def get_concatenated_features():
    return sp.hstack([get_title_desc_vector(),
                      get_useful_features_dict()])

# Turns groups in charge into numbered fields
def get_encoded_gic(prontos_collection = MongoClient().prontosdb.prontos_collection):
    groupsInCharge = []
    for pronto in prontos_collection.find({}):
        groupsInCharge.append(pronto["groupInCharge"].split('_', 1)[0])
    
    le = preprocessing.LabelEncoder()
    return le.fit_transform(groupsInCharge)

def get_encoded_state(prontos_collection = MongoClient().prontosdb.prontos_collection):
    state_list=[]
    for pronto in prontos_collection.find({}):
       state_list.append(pronto["state"])
    
    le = preprocessing.LabelEncoder()
    return le.fit_transform(state_list)

title_desc_vec = get_title_desc_vector()
enc_states = get_encoded_state()
# Split the data into train and test
x_train, x_test, y_train, y_test = train_test_split(title_desc_vec.toarray(), enc_states, test_size = 0.3)

# MultinomialNB for accuracy
mnb = MultinomialNB()
mnb.fit(x_train, y_train)
accuracy = mnb.score(x_test, y_test)

print("Accuracy: {}".format(accuracy))

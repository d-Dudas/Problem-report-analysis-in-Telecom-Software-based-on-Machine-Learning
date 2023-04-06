from pymongo import MongoClient
import nltk
import TfidfVector
from sklearn.feature_extraction import DictVectorizer
import scipy.sparse as sp
from sklearn import preprocessing
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
import numpy as np
from sklearn.impute import SimpleImputer


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

# print("Matrix shape: {}".format(get_title_desc_vector().shape))

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

# Return the concatenated features and eliminate all NaN elements from it
def get_concatenated_features():
    imputer=SimpleImputer(missing_values=np.nan, strategy='mean')
    return imputer.fit_transform(sp.hstack([get_title_desc_vector(),
                      get_useful_features_dict()]))

# Turns groups in charge into numbered fields
def get_encoded_groups_in_charge(prontos_collection = MongoClient().prontosdb.prontos_collection):
    groupsInCharge = []
    for pronto in prontos_collection.find({}):
        groupsInCharge.append(pronto["groupInCharge"])
    

    le = preprocessing.LabelEncoder()
    le.fit_transform(groupsInCharge)

    return le

#Get the data used for testing
def get_tested_data(prontos_collection = MongoClient().prontosdb.prontos_collection):
    state_data=[]
    for pronto in prontos_collection.find({}):
        state_data.append(pronto["state"])
    le=preprocessing.LabelEncoder()
    #transform le from Label to 1D array
    return le.fit_transform(state_data)

#train the ml-algorithm whitch uses the Gaussian approach
def train_ml(clf=GaussianNb(),x=get_concatenated_features(),y=get_tested_data):
    clf.fit(x,y)
    return clf


"""
x=get_concatenated_features().toarray()
y=get_tested_data()
clf=train_ml(x,y)

y_pred=clf.predict([x[0]])
y_test=[y[0]]
print(accuracy_score(y_test,y_pred))"""
from pymongo import MongoClient
import nltk
import TfidfVector
from sklearn.feature_extraction import DictVectorizer
import scipy.sparse as sp
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB

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


# def label_encode_gic(prontos_collection = MongoClient().prontosdb.prontos_collection):
#     gic_list = []
#     cursor = prontos_collection.find({})
#     for document in cursor:
#         gic = document['groupInCharge'].split('_',1)[0]
#         print(gic)
#         if (gic != 'MANO' and gic !='BOAM'):
#             print("T")
#             gic_list.append('not_boam')
#         else:
#             print("F")
#             if gic == 'MANO':
#                 gic_list.append('BOAM')
#             else:
#                 gic_list.append(gic)            
#     for gic in set(gic_list):
#         print(gic)
#     label_encoder = preprocessing.LabelEncoder()
#     encoded_gic = label_encoder.fit_transform(gic_list)
#     return encoded_gic

title_desc_vec = get_title_desc_vector()
gic = get_encoded_gic()
x_train, x_test, y_train, y_test = train_test_split(title_desc_vec.toarray(), gic, test_size=0.3)
gnb = GaussianNB()
y_pred = gnb.fit(x_train, y_train).predict(x_test)
print("Number of mislabeled points out of a total %d points : %d"
           % (x_test.shape[0], (y_test != y_pred).sum()))


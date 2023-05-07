import time
import nltk
import scipy.sparse as sp
from threading import Thread
import read_data_from_db as rdb
import save_and_load_data as sld
from sklearn import preprocessing
from sklearn.naive_bayes import GaussianNB
from nltk.stem.snowball import SnowballStemmer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

last_ml_model_update = time.time()
re_train_ml_model_thread = None

#Filter and keep only the words that are in the english dictionary
def filter_tokens(tokenized_descriptions):
    english_words = set(nltk.corpus.words.words())
    valid_tokens_list = []
    for tokens in tokenized_descriptions:
        # Create a new list to store the valid English words for this description
        valid_tokens = []
        # Loop through each token in the list
        for token in tokens:
            # Check if the token is a valid English word
            if token.lower() in english_words:
                # If it is, add it to the valid_tokens list
                valid_tokens.append(token)
        # Add the list of valid tokens for this description to the valid_tokens_list
        valid_tokens_list.append(valid_tokens)

    return valid_tokens_list

# Stemm each token from the tokenized descriptions list
def stemm_tokens(tokenized_descriptions, stemmer = nltk.PorterStemmer()):
    # The stemmed tokens will be stored in the following array
    stemmed_descriptions = []
    stemmer = SnowballStemmer("english")
    for iter in tokenized_descriptions:
        stemmed_descriptions.append([stemmer.stem(t) for t in iter])

    return stemmed_descriptions

# Rejoin stemmed tokens
def rejoin_processed_tokens(tokens_list):
    # The rejoined text is stored in the following array
    stemmed_text = []
    for tokens in tokens_list:
        stemmed_text.append(" ".join(tokens))
    
    return stemmed_text

# stemmed_text - result of rejoin_processed_tokens()
def get_tfidfVector(stemmed_text):
    # Vectorize the stemmed text
    vectorizer = TfidfVectorizer(stop_words='english')
    return vectorizer.fit_transform(stemmed_text), vectorizer

def fget_tfidfVector(stemmed_text):
    # Vectorize the stemmed text
    f = TfidfVectorizer(stop_words='english')
    return f, f.fit(stemmed_text)

# Returned the processed pronto title and descriptions
# stored in form of a tfidf vector
def get_title_desc_vector():
    return get_tfidfVector(
            rejoin_processed_tokens(
                stemm_tokens(
                    filter_tokens(
                        rdb.get_tokenized_title_and_description()
                    )
                )
            )
        )

# Thats for new prontos
def prepare_tdv(aux):
    return rejoin_processed_tokens(
            stemm_tokens(
                filter_tokens(
                    [nltk.word_tokenize(aux)]
                )
            )
        )

# Return a dict vectorized list
# use with useful features list
def get_dict_vector(data_list):
    dict_vectorizer = DictVectorizer(sparse=True)
    return dict_vectorizer.fit_transform(data_list), dict_vectorizer

# Returns encoded data
def encode_data(data):
    label_encoder = preprocessing.LabelEncoder()
    return label_encoder.fit_transform(data), label_encoder

def get_fast_prediction(pronto):

    vectorizer = sld.deserialize_object("vectorizer.pickle")
    dict_vectorizer = sld.deserialize_object("dict_vectorizer.pickle")
    label_encoder = sld.deserialize_object("label_encoder.pickle")
    ml_model = sld.deserialize_object("MLmodel.pickle")
    accuracy = sld.deserialize_object("accuracy.pickle")
    # get the necesarry data from ponto
    pronto_title_and_desc_vec = vectorizer.transform(prepare_tdv(pronto["title"] + " " + pronto["description"]))
    pronto_useful_feature_list = dict_vectorizer.transform([{"feature": pronto["feature"], "groupInCharge": pronto["groupInCharge"], "release": pronto["release"]}])

    # concatenate the vectors
    pronto_input = sp.hstack([pronto_title_and_desc_vec, pronto_useful_feature_list])

    # get prediction
    prediction = ml_model.predict(pronto_input.toarray())

    # "translate" prediction
    prediction = label_encoder.inverse_transform(prediction)

    try_retrain_ml_model()

    return prediction[0], accuracy

def try_retrain_ml_model():
    current_time = time.time()
    global last_ml_model_update
    global re_train_ml_model_thread
    if((current_time - last_ml_model_update) / 3600 >= 72 and (re_train_ml_model_thread is None or not re_train_ml_model_thread.is_alive())):
        last_ml_model_update = current_time
        re_train_ml_model_thread = Thread(target=re_train_ml_model, args=())
        re_train_ml_model_thread.start()
    else:
        print("The ML model was updated in the last 72 hours, or the update is still running")

def try_retrain_ml_model_now():
    global last_ml_model_update
    global re_train_ml_model_thread
    if re_train_ml_model_thread is None or not re_train_ml_model_thread.is_alive():
        last_ml_model_update = time.time()
        re_train_ml_model_thread = Thread(target=re_train_ml_model, args=())
        re_train_ml_model_thread.start()
    else:
        print("The ML model is already updating...")

def re_train_ml_model():
    # Read the data from database and save the new processed data
    print("Retraining ML model")
    title_and_desc_vec, vectorizer = get_title_desc_vector()
    sld.save_sparse_matrix("title_and_desc_vec.npz", title_and_desc_vec)
    sld.serialize_object("vectorizer.pickle", vectorizer)

    useful_feature_list, dict_vectorizer = get_dict_vector(rdb.get_useful_features_list())
    sld.save_sparse_matrix("useful_feature_list.npz", useful_feature_list)
    sld.serialize_object("dict_vectorizer.pickle", dict_vectorizer)

    encoded_states, label_encoder = encode_data(rdb.get_encoded_state())
    sld.serialize_object("encoded_states.pickle", encoded_states)
    sld.serialize_object("label_encoder.pickle", label_encoder)

    # Prepare the input for the ml model
    model_input = sp.hstack([title_and_desc_vec, useful_feature_list])

    # Split the data into test and train sets
    x_train, x_test, y_train, y_test = train_test_split(model_input.toarray(), encoded_states, test_size = 0.7, random_state=50)

    # Prepare the ml model and save the trained model and its accuracy
    ml_model = GaussianNB()
    ml_model.fit(x_train, y_train)
    accuracy = ml_model.score(x_test, y_test)
    sld.serialize_object("MLmodel.pickle", ml_model)
    sld.serialize_object("accuracy.pickle", accuracy)

    print("ML model retrained.")

def upload_pronto(pronto):
    if sld.upload_pronto(pronto):
        try_retrain_ml_model_now()

try_retrain_ml_model_now()
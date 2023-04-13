import nltk
import scipy.sparse as sp
import read_data_from_db as rdb
import save_and_load_data as sld
from sklearn import preprocessing
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

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
    return TfidfVectorizer(stop_words='english').fit_transform(stemmed_text)

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

def get_desc_vector():
    return get_tfidfVector(
            rejoin_processed_tokens(
                stemm_tokens(
                    filter_tokens(
                        rdb.get_tokenized_descriptions()
                    )
                )
            )
        )

# Return a dict vectorized list
# use with useful features list
def get_dict_vector(data_list):
    return DictVectorizer(sparse=True).fit_transform(data_list)

# Concatenates features
def concatenate_features():
    useful_features_dict = get_dict_vector(rdb.get_useful_features_list())
    return sp.hstack([get_title_desc_vector(),
                      useful_features_dict])

# Returns encoded data
def encode_data(data):
    return preprocessing.LabelEncoder().fit_transform(data)

def get_multinomialMB():
    enc_states = sld.deserialize_object("encoded_states.pickle")
    title_desc_vec = sld.load_sparse_matrix("title_desc_vec.npz")
    x_train, x_test, y_train, y_test = train_test_split(title_desc_vec.toarray(), enc_states, test_size = 0.5)
    # MultinomialNB for accuracy
    mnb = MultinomialNB()
    mnb.fit(x_train, y_train)
    
    return mnb

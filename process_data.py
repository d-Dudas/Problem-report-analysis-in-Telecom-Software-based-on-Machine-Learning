import nltk
import read_data_from_db as rdb
import scipy.sparse as sp
from sklearn import preprocessing
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

def get_title_desc_vector():
    return get_tfidfVector(
            get_rejoined_processed_tokens(
                get_stemmed_tokens(
                    get_filtered_tokens(
                        rdb.get_tokenized_title_and_description()
                    )
                )
            )
        )

def get_dict_vector(data_list):
    return DictVectorizer(sparse=True).fit_transform(data_list)

def get_concatenated_features():
    useful_features_dict = get_dict_vector(rdb.get_useful_features_list())
    return sp.hstack([get_title_desc_vector(),
                      useful_features_dict])

def get_encoded_data(data):
    return preprocessing.LabelEncoder().fit_transform(data)

#Filter and keep only the words that are in the english dictionary
def get_filtered_tokens(tokenized_descriptions):
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
def get_stemmed_tokens(tokenized_descriptions, stemmer = nltk.PorterStemmer()):
    # The stemmed tokens will be stored in the following array
    stemmed_descriptions = []
    for iter in tokenized_descriptions:
        stemmed_descriptions.append([stemmer.stem(t) for t in iter])

    return stemmed_descriptions

# Rejoin stemmed tokens
def get_rejoined_processed_tokens(tokens_list):
    # The rejoined text is stored in the following array
    stemmed_text = []
    for tokens in tokens_list:
        stemmed_text.append(" ".join(tokens))
    
    return stemmed_text

def get_tfidfVector(stemmed_text):
    # Vectorize the stemmed text
    return TfidfVectorizer(stop_words='english').fit_transform(stemmed_text)

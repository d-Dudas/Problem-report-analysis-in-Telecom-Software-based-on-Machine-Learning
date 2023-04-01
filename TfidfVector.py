import nltk
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer

# Get each pronto's description and tokenize it
def get_tokenized_prontos_descriptions(prontos_collection = MongoClient().prontosdb.prontos_collection):
    # The tokenized descriptions are stored in the following array
    tokenized_prontos_descriptions = []
    for pronto in prontos_collection.find({}):
        tokenized_prontos_descriptions.append(nltk.word_tokenize(pronto["description"]))
    
    return tokenized_prontos_descriptions

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

# tokenized_descriptions = get_tokenized_prontos_descriptions()
# print("Tokens ready")
# tokenized_descriptions = get_filtered_tokens(tokenized_descriptions)
# print("Filtered")
# stemmed_tokens = get_stemmed_tokens(tokenized_descriptions)
# print("Stemmed.")
# stemmed_text = get_rejoined_processed_tokens(stemmed_tokens)
# print("Rejoined")
# matrix = get_tfidfVector(stemmed_text)

# print("Matrix shape: {}".format(matrix.shape))

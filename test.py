import sys
import nltk
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import words

# Acces the prontos collection
prontos_collection = MongoClient().prontosdb.prontos_collection

# Get each pronto's description and tokenize it
# The tokenized descriptions are stored in the following array
tokenized_prontos_descriptions = []

print("Tokenizing each pronto's description...")

for pronto in prontos_collection.find({}):
    tokenized_prontos_descriptions.append(nltk.word_tokenize(pronto["description"]))
print("Tokenization done.")


#Verify if the words are in the english dictionary
english_words = set(words.words())
valid_tokens_list = []
for tokens in tokenized_prontos_descriptions:
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


# Stemming each token with PorterStemmer
stemmer = nltk.PorterStemmer()
# The stemmed tokens will be stored in the following array
stemmed_tokens = []

print("Porter stemming each token...")

for pronto in valid_tokens_list:
    stemmed_tokens.append([stemmer.stem(t) for t in pronto])
print("Porter stemming done.")

# Rejoin stemmed tokens
# The rejoined text is stored in the following array
stemmed_text = []

print("Rejoining stemmed tokens...")

for st in stemmed_tokens:
    stemmed_text.append(" ".join(st))
print("Rejoin done.")


"""for text in stemmed_text:
    print(text,end='\n\n\n\n\n')
"""
# Vectorize the stemmed text
vectorizer = TfidfVectorizer(stop_words='english')
# The result is stored in the following matrix
matrix = vectorizer.fit_transform(stemmed_text)

print("Vectorizing done.")

print("Matrix shape: {}".format(matrix.shape))

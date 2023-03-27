import sys
import nltk
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer

# Acces the prontos collection
prontos_collection = MongoClient().prontosdb.prontos_collection

# Get each pronto's description and tokenize it
# The tokenized descriptions are stored in the following array
tokenized_prontos_descriptions = []

print("Tokenizing each pronto's description...")

for pronto in prontos_collection.find({}):
    tokenized_prontos_descriptions.append(nltk.word_tokenize(pronto["description"]))
print("Tokenization done.")

# Stemming each token with PorterStemmer
stemmer = nltk.PorterStemmer()
# The stemmed tokens will be stored in the following array
stemmed_tokens = []

print("Porter stemming each token...")

for pronto in tokenized_prontos_descriptions:
    stemmed_tokens.append([stemmer.stem(t) for t in pronto])
print("Porter stemming done.")

stemmer = nltk.LancasterStemmer()
print("Lancaster stemming each token...")

for pronto in tokenized_prontos_descriptions:
    stemmed_tokens.append([stemmer.stem(t) for t in pronto])
print("Lancaster stemming done.")

# Rejoin stemmed tokens
# The rejoined text is stored in the following array
stemmed_text = []

print("Rejoining stemmed tokens...")

for st in stemmed_tokens:
    stemmed_text.append(" ".join(st))
print("Rejoin done.")

# Vectorize the stemmed text
vectorizer = TfidfVectorizer(stop_words='english')
# The result is stored in the following matrix
matrix = vectorizer.fit_transform(stemmed_text)

print("Vectorizing done.")

print("Matrix shape: {}".format(matrix.shape))

for fn in vectorizer.get_feature_names_out():
    print(fn, file = sys.stderr)

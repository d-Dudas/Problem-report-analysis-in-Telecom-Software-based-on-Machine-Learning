import pickle
from scipy.sparse import save_npz, load_npz
from pymongo import MongoClient
import pymongo

def save_sparse_matrix(filename, matrix):
    filename = "./serialized_data/" + filename
    save_npz(filename, matrix)

def load_sparse_matrix(filename):
    filename = "./serialized_data/" + filename

    return load_npz(filename)

def serialize_object(filename, data):
    filename = "./serialized_data/" + filename
    with open(filename, 'wb') as f:
        pickle.dump(data, f)

def deserialize_object(filename):
    filename = "./serialized_data/" + filename
    with open(filename, 'rb') as f:
        object = pickle.load(f)

    return object

def upload_pronto(pronto):
    prontos_collection = MongoClient('mongodb://db:27017').prontosdb.prontos_collection
    uploaded = False
    try:
        rez = prontos_collection.insert_one(pronto)
        print("Inserted pronto: {}".format(rez.inserted_id))
        uploaded = True
    except pymongo.errors.DuplicateKeyError:
        print("Duplicated key error for = {}".format(value['title']))

    return uploaded

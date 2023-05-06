import pickle
from scipy.sparse import save_npz, load_npz
from pymongo import MongoClient
import pymongo



def save_sparse_matrix(filename, matrix):
    filename = "./data/" + filename
    save_npz(filename, matrix)

def load_sparse_matrix(filename):
    filename = "./data/" + filename
    return load_npz(filename)

def serialize_object(filename, enc_data):
    filename = "./data/" + filename
    with open(filename, 'wb') as f:
        pickle.dump(enc_data, f)

def deserialize_object(filename):
    filename = "./data/" + filename
    with open(filename, 'rb') as f:
        object = pickle.load(f)
    return object

def upload_pronto(pronto):
    prontos_collection = MongoClient().prontosdb.prontos_collection
    uploaded = None
    try:
        rez = prontos_collection.insert_one(pronto)
        print("Inserted pronto: {}".format(rez.inserted_id))
        uploaded = True
    except pymongo.errors.DuplicateKeyError:
        print("Duplicated key error for problemReportId = {}".format(pronto["problemReportId"]))
        uploaded = False

    return uploaded

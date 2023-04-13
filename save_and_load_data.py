import pickle
from scipy.sparse import save_npz, load_npz

def save_sparse_matrix(filename, matrix):
    save_npz(filename, matrix)

def load_sparse_matrix(filename):
    return load_npz(filename)

def serialize_object(filename, enc_data):
    with open(filename, 'wb') as f:
        pickle.dump(enc_data, f)

def deserialize_object(filename):
    with open(filename, 'rb') as f:
        object = pickle.load(f)
    return object

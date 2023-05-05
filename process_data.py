import nltk
import numpy as np
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

def fget_title_desc_vector():
    return fget_tfidfVector(
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
    dict_vectorizer = DictVectorizer(sparse=True)
    return dict_vectorizer.fit_transform(data_list), dict_vectorizer

def fget_dict_vector(data_list):
    d = DictVectorizer(sparse=True)
    return d, d.fit(data_list)

# Concatenates features
def concatenate_features():
    useful_features_dict = get_dict_vector(rdb.get_useful_features_list())
    return sp.hstack([get_title_desc_vector(),
                      useful_features_dict])

# Returns encoded data
def encode_data(data):
    label_encoder = preprocessing.LabelEncoder()
    return label_encoder.fit_transform(data), label_encoder

def get_multinomialMB(pronto):
    enc_states = sld.deserialize_object("encoded_states.pickle")
    y = sld.load_sparse_matrix("title_desc_vec.npz")
    v, title_desc_vec = fget_title_desc_vector()
    d, usf2 = fget_dict_vector(rdb.get_useful_features_list())
    x_train, x_test, y_train, y_test = train_test_split(y.toarray(), enc_states, test_size = 0.5)
    uf = d.transform([{"feature": pronto["feature"], "groupInCharge": pronto["groupInCharge"], "release": pronto["release"]}])
    tdv = v.transform(prepare_tdv(pronto["title"] + " " + pronto["description"]))

    # x = sp.hstack([tdv, uf])
    # x = sp.hstack([tdv, uf])
    # tdva = title_desc_vec.transform(tdv)
    # MultinomialNB for accuracy
    mnb = MultinomialNB()
    mnb.fit(x_train, y_train)

    pr = mnb.predict(tdv)
    le, aux = encode_data(rdb.get_encoded_state())
    print(le.inverse_transform(pr))
    
    return mnb

pronto = {
  "_id": {
    "$oid": "64175dbaffad73407afc6b3b"
  },
  "problemReportId": "PR493986",
  "faultAnalysisId": [
    "FA562744"
  ],
  "attachedPRs": [],
  "author": "Steta, Mihail (Nokia - RO/Timisoara)",
  "build": "SBTS19B_ENB_0000_000827_000000",
  "description": "*** DEFAULT TEMPLATE for 2G-3G-4G-5G-SRAN-FDD-TDD-DCM-Micro-Controller common template v1.1.0 (09.05.2018) – PLEASE FILL IT IN BEFORE CREATING A PR AND DO NOT CHANGE / REMOVE ANY SECTION OF THIS TEMPLATE ***\r\n\r\n[1. Detail Test Steps:]\r\n1.SWR started\r\n2. Check SBTS state after software replacement\r\n\r\n[2. Expected Result:]\r\n\r\n1. SBTS on air\r\n2. All cells on air\r\n3. No unnexpected alarms present\r\n\r\n[3. Actual Result:]\r\n1. Ok\r\n2. NOK . 2 WCDMA cells and one LTE cell are down\r\n\r\n[4. Tester analysis:]\r\n\r\nAnalysis of Logs: 2 WCDMA cells and on LTE cell are down after Softare replacement. All cells are mapped on the same RFM, FRGB type. \r\n\r\nNo alarms raised, nothing relevant found in traces despite the issue is permanent.\r\n\r\nAction performed to recover:\r\n- after RFM reset - same isue;\r\n- after RFM block/unblock - same issue;\r\nOnly SBTS reset solve the issue, all cells are on air.\r\n\r\nSWBOT information:\r\nMANO_WRO_HWMGMT 40%\r\nMANO_TIM_FMRECOV 40%\r\n\r\n\r\n\r\n\r\n[5. Log(s) file name containing a fault: (clear indication (exact file name) and timestamp where fault can be found in attached logs)]\r\n\\\\eseefsn50.emea.nsn-net.net\\rotta4internal\\HetRAN\\msteta\\Cells down after SWR from 19A to 19B\r\n\r\n[6. Test-Line Reference/used HW/configuration/tools/SW version]\r\nSBTS10152\r\n1LW2_1.1.1_FRGY_1x6G_IA_1_444;1LW2_1.1.2_FRGY_1x6G_IA_1_444;1LW2_1.1.3_FRGY_1x6G_IA_1_444;B1FLW_1+B\r\n\r\nBase build: SBTS19A_ENB_0000_000229_445911 \r\nTarget build: SBTS19B_ENB_0000_000827_000000\r\n\r\n[7. Used Flags: (list here used R&D flags)]\r\nun swconfig\r\n\r\n[8. Fault Occurrence Rate:]\r\n   How many times Test Scenario was run?\r\n1\r\n   How many times fault was reproduced?\r\n1\r\n   How many sites in the same live operation was run in case of customer fault? \r\nN/A \r\n\r\n[9. Test Scenario History of Execution: (what was changed since it was tested successfully for the last time)]\r\n   Was Test Scenario passing before?\r\nyes\r\n   What was the last SW version Test Scenario was passing?\r\nSBTS19B_ENB_0000_000734_000000\r\n   Were there any differences between test-lines since last time Test Scenario was passing?\r\nno\r\n   Were there any changes in Test Scenario since last run it passed?\r\nno\r\n[10. Test Case Reference: (QC, RP or UTE link)]\r\nnot needed in documentation, specification made fault reports and customer made tickets\r\n\r\n*** END OF DEFAULT TEMPLATE ***",
  "feature": "System_Operability",
  "groupInCharge": "MANO_MNL_RADIOCTRL",
  "state": "Correction Not Needed",
  "title": "[SBTS19B][CIT][FSM] 2 WCDMA cells and one LTE cell are down after SWR from SBTS19A to SBTS19B",
  "authorGroup": "NITSIVBTS8",
  "informationrequestID": [
    "IR158069"
  ],
  "statusLog": '',
  "release": [
    "SBTS19B"
  ],
  "explanationforCorrectionNotNeeded": [
    "Pronto was not reproducible with same build in IR request by FRI. Author agreed to set PR as CNN-FNR"
  ],
  "reasonWhyCorrectionisNotNeeded": [
    "Fault was not reproducible"
  ],
  "faultAnalysisFeature": [],
  "faultAnalysisGroupInCharge": [
    "MANO_MNL_RADIOCTRL"
  ],
  "stateChangedtoClosed": '',
  "faultAnalysisTitle": [
    "[SBTS19B][CIT][FSM] 2 WCDMA and one LTE cells remaind down after SWR from SBTS19A to SBTS19B failed"
  ]
}

# get_multinomialMB(pronto)

# 

def get_prediction(pronto):
    # first, get the title and description
    # vector, from db or ./data/
    # title_and_desc_vec, vectorizer = get_title_desc_vector()
    # sld.save_sparse_matrix("title_and_desc_vec.npz", title_and_desc_vec)
    # sld.serialize_object("vectorizer.pickle", vectorizer)
    title_and_desc_vec = sld.load_sparse_matrix("title_and_desc_vec.npz")
    vectorizer = sld.deserialize_object("vectorizer.pickle")

    print("Title and desc vector loaded...")

    # get the useful feature list dict vector
    # from db or ./data/
    # useful_feature_list, dict_vectorizer = get_dict_vector(rdb.get_useful_features_list())
    # sld.save_sparse_matrix("useful_feature_list.npz", useful_feature_list)
    # sld.serialize_object("dict_vectorizer.pickle", dict_vectorizer)

    useful_feature_list = sld.load_sparse_matrix("useful_feature_list.npz")
    dict_vectorizer = sld.deserialize_object("dict_vectorizer.pickle")

    print("Useful feature list vector loaded...")

    # get encoded states
    # encoded_states, label_encoder = encode_data(rdb.get_encoded_state())
    # sld.serialize_object("encoded_states.pickle", encoded_states)
    # sld.serialize_object("label_encoder.pickle", label_encoder)

    encoded_states = sld.deserialize_object("encoded_states.pickle")
    label_encoder = sld.deserialize_object("label_encoder.pickle")

    print("Ecoded states loaded...")

    # concatenate title and desc vector with useful feature list
    model_input = sp.hstack([title_and_desc_vec, useful_feature_list])

    print("Vectors concatenated...")

    # split the data into training and test parts
    x_train, x_test, y_train, y_test = train_test_split(model_input.toarray(), encoded_states, test_size = 0.7, random_state=42)

    print("Split done...")

    # train the model
    mnb = MultinomialNB()
    mnb.fit(x_train, y_train)
    accuracy = mnb.score(x_test, y_test)

    print("Model trained...")
    print("Score: " + str(accuracy))

    # get the necesarry data from ponto
    pronto_title_and_desc_vec = vectorizer.transform(prepare_tdv(pronto["title"] + " " + pronto["description"]))
    pronto_useful_feature_list = dict_vectorizer.transform([{"feature": pronto["feature"], "groupInCharge": pronto["groupInCharge"], "release": pronto["release"]}])

    print("Data extracted from pronto")

    # concatenate the vectors
    pronto_input = sp.hstack([pronto_title_and_desc_vec, pronto_useful_feature_list])

    print("Pronto input prepared...")

    # get prediction
    prediction = mnb.predict(pronto_input)

    print("Prediction1:")

    # "translate" prediction
    prediction = label_encoder.inverse_transform(prediction)

    print(prediction)

    # r = {"prediction": prediction[0], "accuracy": accuracy}
    # print(r)
    return prediction[0], accuracy

# get_prediction(pronto)
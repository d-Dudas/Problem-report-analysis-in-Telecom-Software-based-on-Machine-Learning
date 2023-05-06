import json
from flask import Flask, jsonify, request
from process_data import get_fast_prediction, upload_pronto

app = Flask(__name__)

necessary_keys = [
                  "description",
                  "feature",
                  "groupInCharge",
                  "title",
                  "release"
                  ]

valid_keys = ["problemReportId",
                  "faultAnalysisId",
                  "attachedPRs",
                  "author",
                  "build",
                  "description",
                  "feature",
                  "groupInCharge",
                  "state",
                  "title",
                  "authorGroup",
                  "informationrequestID",
                  "statusLog",
                  "release",
                  "explanationforCorrectionNotNeeded",
                  "reasonWhyCorrectionisNotNeeded",
                  "faultAnalysisFeature",
                  "faultAnalysisGroupInCharge",
                  "stateChangedtoClosed",
                  "faultAnalysisTitle"
                  ]

def is_valid_for_prediction(pronto):
    is_valid = True
    for key in necessary_keys:
        if key not in list(pronto.keys()):
            is_valid = False
    
    return is_valid

def is_valid_pronto(pronto):
    return list(pronto.keys()) == valid_keys

def create_pronto_object(file):  
    pronto = {}
    for key in file.keys():
        pronto[key] = file[key]

    state, accuracy = get_fast_prediction(pronto)
    pronto["state"] = state
    pronto["accuracy"] = accuracy
    pronto["saved"] = False
    pronto["isValid"] = is_valid_pronto(file)

    return pronto

@app.route('/receive-data', methods=['POST'])
def receive_data():
    data = request.json
    print(data)
    data = create_pronto_object(data)

    return jsonify(data)

@app.route('/save-pronto', methods=['POST'])
def save_pronto():
    data = request.json
    aux = {}
    for key in valid_keys:
        aux[key] = data[key]
    print(aux)
    upload_pronto(aux)
    data = {'msg': 'Pronto saved'}

    return jsonify(data)

@app.route('/receive-files', methods=['POST'])
def receive_file():
    files = request.files.getlist('files[]')
    response = []
    for file in files:
        file_contents = json.loads(file.read().decode('utf8').replace("'", '"'))
        if(isinstance(file_contents, list)):
            for f in file_contents:
                if is_valid_for_prediction(f):
                    response.append(create_pronto_object(f))
        else:
            if is_valid_for_prediction(file_contents):
                response.append(create_pronto_object(file_contents))
    return(response)

if __name__ == '__main__':
    app.run()

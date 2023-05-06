import json
import process_data as pd
from flask import Flask, jsonify, request

app = Flask(__name__)

def is_valid_for_prediction(pronto):
    necessary_keys = [
                  "description",
                  "feature",
                  "groupInCharge",
                  "title",
                  "release"
                  ]

    is_valid = True
    for key in necessary_keys:
        if key not in list(pronto.keys()):
            is_valid = False
    
    return is_valid

def is_valid_pronto(pronto):
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
    
    return list(pronto.keys()) == valid_keys

def create_pronto_object(file):
    problemReportId = file['problemReportId']
    title = file['title']
    release = file['release']
    feature = file['feature']
    gic = file['groupInCharge']
    descriere = file['description']
    saved = False

    pronto = {
            "problemReportId": problemReportId,
            "title": title,
            "release": release,
            "feature": feature,
            "groupInCharge": gic,
            "description": descriere,
            "state": "Ana are mere",
            "saved": saved
        }

    state, accuracy = pd.get_fast_prediction(pronto)
    pronto["state"] = state
    pronto["accuracy"] = accuracy
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
    print(data)
    data = {'msg': 'Ana are mere'}

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

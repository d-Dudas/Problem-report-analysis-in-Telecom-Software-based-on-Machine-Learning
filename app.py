from flask import Flask, jsonify, request
import json
# import sys
# sys.path.append('../../Problem-report-analysis-in-Telecom-Software-based-on-Machine-Learning')
# sys.path.append('../../Problem-report-analysis-in-Telecom-Software-based-on-Machine-Learning/data/')
import process_data as pd

app = Flask(__name__)

@app.route('/api/data')
def get_data():
    data = {'message': 'Hello from the Flask API!', 'msg': 'Ana are mere!'}
    return jsonify(data)

@app.route('/receive-data', methods=['POST'])
def receive_data():
    data = request.json
    print(data)
    data = create_pronto_object(data)
    import time
    time.sleep(3)
    # Do something with the data
    return jsonify(data)

@app.route('/save-pronto', methods=['POST'])
def save_pronto():
    data = request.json
    print(data)
    data = {'msg': 'Ana are mere'}
    import time
    time.sleep(3)
    # Do something with the data
    return jsonify(data)

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

    state, accuracy = pd.get_prediction(pronto)
    pronto["state"] = state
    pronto["accuracy"] = accuracy
    return pronto

@app.route('/receive-files', methods=['POST'])
def receive_file():
    files = request.files.getlist('files[]')
    response = []
    for file in files:
        file_contents = json.loads(file.read().decode('utf8').replace("'", '"'))
        if(isinstance(file_contents, list)):
            for f in file_contents:
                response.append(create_pronto_object(f))
        else:
            response.append(create_pronto_object(file_contents))
    return(response)

if __name__ == '__main__':
    app.run()

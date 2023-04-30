from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/data')
def get_data():
    data = {'message': 'Hello from the Flask API!', 'msg': 'Ana are mere!'}
    return jsonify(data)

@app.route('/receive-data', methods=['POST'])
def receive_data():
    data = request.json
    print(data)
    data = {'msg': 'Ana are mere'}
    import time
    time.sleep(3)
    # Do something with the data
    return jsonify(data)

if __name__ == '__main__':
    app.run()

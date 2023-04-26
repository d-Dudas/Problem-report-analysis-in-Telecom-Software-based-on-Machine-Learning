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
    # Do something with the data
    return({})

if __name__ == '__main__':
    app.run()

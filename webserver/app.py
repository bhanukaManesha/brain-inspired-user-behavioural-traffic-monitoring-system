#!flask/bin/python
import sys
sys.path.insert(0, '../ai_module/inference/')

from flask import Flask, jsonify,request

from main import inference_data

app = Flask(__name__)


@app.route('/data', methods=['GET'])
def feedback():
    return "Done"

@app.route('/data', methods=['POST'])
def receive_data():
    # print (request.is_json)
    content = request.get_json()
    # print (content)
    inference_data(content["data"])
    return 'JSON posted'


if __name__ == '__main__':
    app.run(debug=True)


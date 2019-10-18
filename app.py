from flask import Flask, request, jsonify
from utils.faceRec import *

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/recognition', methods=['POST'])
def faceRe():
    image_path = request.form['image_path']
    flag = ifContainFace(image_path)
    if isinstance(flag, str):
        return jsonify({'error': flag})
    else:
        return jsonify({'result': ifInDB(flag)})

if __name__ == '__main__':
    app.run()

from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import base64
from rps_logic import RPSLogic

app = Flask(__name__)
rps = RPSLogic()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    image1 = decode_base64(data['player1'])
    image2 = decode_base64(data['player2'])

    result = rps.play_round(image1, image2)
    return jsonify(result)

def decode_base64(data):
    header, encoded = data.split(',', 1)
    img = base64.b64decode(encoded)
    np_arr = np.frombuffer(img, np.uint8)
    return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 5000, debug = True))

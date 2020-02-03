# Serve model as a flask application

import pickle
import numpy as np
import time
from flask import Flask, request

model = None
app = Flask(__name__)


def load_model():
    global model
    # model variable refers to the global variable
    with open('iris_trained_model.pkl', 'rb') as f:
        model = pickle.load(f)


@app.route('/')
def home_endpoint():
    return 'Hello World!'

@app.route('/HealthCheck')
def health_check():
    return 'OK'

@app.route('/predict', methods=['POST'])
def get_prediction():
    start = time.time()
    # Works only for a single sample
    if request.method == 'POST':
        data = request.get_json()  # Get data posted as a json
        print(data)
        data = np.array(data)[np.newaxis, :]  # converts shape from (4,) to (1, 4)
        prediction = model.predict(data)  # runs globally loaded model on the data
    end = time.time()
    return str(prediction)+"\n"+"process time"+str(end-start)+"\n"


if __name__ == '__main__':
    load_model()  # load model at the beginning once only
    app.run(host='0.0.0.0', port=80)

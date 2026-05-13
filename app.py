from flask import Flask, request, jsonify
from flask_cors import CORS
from predict import predict_url

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Phishing Detection API is running!"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    url = data.get("url")

    result = predict_url(url)

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)

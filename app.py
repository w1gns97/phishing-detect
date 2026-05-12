from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from predict import predict_url

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    url = data.get("url")
    result = predict_url(url)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)

import os
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from feature_extractor import extract_features

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "rf_model.pkl")
feature_path = os.path.join(BASE_DIR, "feature_names.pkl")

model = joblib.load(model_path)
feature_names = joblib.load(feature_path)

def create_visualization():
    importances = model.feature_importances_
    plt.figure(figsize=(8, 4))
    plt.barh(feature_names, importances)
    plt.title("Feature Importance")
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    plt.close()
    buffer.seek(0)

    return base64.b64encode(buffer.getvalue()).decode()

def predict_url(url):
    features = extract_features(url)
    df = pd.DataFrame([features])

    for col in feature_names:
        if col not in df.columns:
            df[col] = 0

    df = df[feature_names]

    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0]

    result = "정상 사이트" if prediction == 1 else "피싱 사이트"

    return {
        "result": result,
        "normal_prob": round(probability[1] * 100, 2),
        "phishing_prob": round(probability[0] * 100, 2),
        "feature_plot": create_visualization(),
        "features": features
    }

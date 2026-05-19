import os
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import base64

from io import BytesIO
from feature_extractor import extract_features

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = joblib.load(os.path.join(BASE_DIR, "rf_model.pkl"))
feature_names = joblib.load(os.path.join(BASE_DIR, "feature_names.pkl"))

FEATURE_DESCRIPTIONS = {
    "having_IPhaving_IP_Address": "IP Address Usage",
    "URLURL_Length": "Long URL Length",
    "Shortining_Service": "Shortened URL",
    "having_At_Symbol": "@ Symbol Usage",
    "double_slash_redirecting": "Redirect // Usage",
    "Prefix_Suffix": "Hyphen In Domain",
    "having_Sub_Domain": "Too Many Subdomains",
    "SSLfinal_State": "HTTPS Security",
    "Domain_registeration_length": "Short Domain Name",
    "HTTPS_token": "Fake HTTPS In Domain",
    "Request_URL": "Long Request Path",
    "URL_of_Anchor": "Abnormal Anchor",
    "Links_in_tags": "Special Characters",
    "SFH": "Login Keyword",
    "Submitting_to_email": "Email Submission",
    "Redirect": "Multiple Redirects",
    "Iframe": "Iframe Related"
}

def create_visualization(features):

    labels = []
    values = []
    colors = []

    for key, value in features.items():

        if key in FEATURE_DESCRIPTIONS:

            labels.append(FEATURE_DESCRIPTIONS[key])

            values.append(value)

            if value == -1:
                colors.append("#ef4444")
            else:
                colors.append("#22c55e")

    plt.figure(figsize=(9, 5))

    bars = plt.barh(
        labels,
        values,
        color=colors
    )

    plt.xlim(-1.2, 1.2)

    plt.xlabel("Risk Score")

    plt.title("URL Security Analysis")

    plt.grid(
        axis='x',
        linestyle='--',
        alpha=0.3
    )

    plt.tight_layout()

    buffer = BytesIO()

    plt.savefig(
        buffer,
        format="png",
        bbox_inches="tight",
        dpi=150
    )

    plt.close()

    buffer.seek(0)

    return base64.b64encode(
        buffer.getvalue()
    ).decode()

def generate_reason(features):

    위험요소 = []
    정상요소 = []

    for key, value in features.items():

        설명 = FEATURE_DESCRIPTIONS.get(key, key)

        if value == -1:
            위험요소.append(설명)

        else:
            정상요소.append(설명)

    return {
        "danger_reasons": 위험요소,
        "safe_reasons": 정상요소
    }

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

    reasons = generate_reason(features)

    return {

        "result": result,

        "normal_prob": round(probability[1] * 100, 2),

        "phishing_prob": round(probability[0] * 100, 2),

        "feature_plot": create_visualization(features),

        "danger_reasons": reasons["danger_reasons"],

        "safe_reasons": reasons["safe_reasons"]
    }

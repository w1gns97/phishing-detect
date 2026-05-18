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
    "having_IPhaving_IP_Address": "IP 주소 사용",
    "URLURL_Length": "긴 URL 길이",
    "Shortining_Service": "단축 URL 사용",
    "having_At_Symbol": "@ 기호 포함",
    "double_slash_redirecting": "// 리다이렉트 사용",
    "Prefix_Suffix": "하이픈(-) 포함 도메인",
    "having_Sub_Domain": "과도한 서브도메인",
    "SSLfinal_State": "HTTPS 보안 사용",
    "Domain_registeration_length": "짧은 도메인 이름",
    "HTTPS_token": "도메인 내 https 문자열 포함",
    "Request_URL": "긴 요청 경로",
    "URL_of_Anchor": "비정상 Anchor 사용",
    "Links_in_tags": "특수 문자 포함",
    "SFH": "로그인 관련 키워드 포함",
    "Submitting_to_email": "이메일 전송 사용",
    "Redirect": "과도한 리다이렉트",
    "Iframe": "iframe 관련 요소 포함"
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
                colors.append("red")
            else:
                colors.append("green")

    plt.figure(figsize=(10, 6))

    plt.barh(labels, values, color=colors)

    plt.xlim(-1.5, 1.5)

    plt.xlabel("위험도 분석")

    plt.title("URL 특징 분석 결과")

    plt.tight_layout()

    buffer = BytesIO()

    plt.savefig(buffer, format="png")

    plt.close()

    buffer.seek(0)

    return base64.b64encode(buffer.getvalue()).decode()

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

import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

from feature_extractor import extract_features

# =========================
# 피싱 사이트 데이터 불러오기
# =========================

print("피싱 데이터 불러오는 중...")

phishing_df = pd.read_csv("dataset2.csv")

phishing_urls = phishing_df["홈페이지주소"].dropna().tolist()

print(f"피싱 URL 개수: {len(phishing_urls)}")

# =========================
# 정상 사이트 데이터 불러오기
# =========================

print("정상 데이터 불러오는 중...")

normal_df = pd.read_csv("dataset3.csv")

# 컬럼명 자동 탐색
possible_cols = [
    "domain",
    "url",
    "URL",
    "homepage",
    "site",
    "주소"
]

normal_col = None

for col in possible_cols:

    if col in normal_df.columns:
        normal_col = col
        break

# 첫 번째 컬럼 fallback
if normal_col is None:
    normal_col = normal_df.columns[0]

normal_urls = normal_df[normal_col].dropna().tolist()

print(f"정상 URL 개수: {len(normal_urls)}")

# =========================
# Feature 생성
# =========================

data = []

print("\n피싱 사이트 Feature 추출 중...")

for idx, url in enumerate(phishing_urls):

    try:

        if not str(url).startswith(("http://", "https://")):
            url = "http://" + str(url)

        features = extract_features(url)

        features["label"] = 0

        data.append(features)

        if idx % 1000 == 0:
            print(f"피싱 처리 중: {idx}")

    except:
        continue

print("\n정상 사이트 Feature 추출 중...")

for idx, url in enumerate(normal_urls):

    try:

        if not str(url).startswith(("http://", "https://")):
            url = "http://" + str(url)

        features = extract_features(url)

        features["label"] = 1

        data.append(features)

        if idx % 1000 == 0:
            print(f"정상 처리 중: {idx}")

    except:
        continue

# =========================
# DataFrame 생성
# =========================

df = pd.DataFrame(data)

print("\n생성된 데이터:")
print(df.head())

print("\n전체 데이터 개수:", len(df))

# =========================
# 학습 데이터 준비
# =========================

X = df.drop("label", axis=1)

y = df["label"]

feature_names = X.columns.tolist()

# =========================
# 학습 / 테스트 분리
# =========================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.2,

    random_state=42,

    stratify=y
)

# =========================
# RandomForest 모델 생성
# =========================

print("\nRandomForest 학습 중...")

model = RandomForestClassifier(

    n_estimators=300,

    max_depth=15,

    min_samples_split=5,

    random_state=42,

    n_jobs=-1
)

# =========================
# 모델 학습
# =========================

model.fit(X_train, y_train)

# =========================
# 예측
# =========================

pred = model.predict(X_test)

# =========================
# 성능 평가
# =========================

accuracy = accuracy_score(y_test, pred)

print(f"\n모델 정확도: {accuracy * 100:.2f}%")

print("\n분류 리포트:")
print(classification_report(y_test, pred))

print("\n혼동 행렬:")
print(confusion_matrix(y_test, pred))

# =========================
# 모델 저장
# =========================

joblib.dump(model, "rf_model.pkl")

joblib.dump(feature_names, "feature_names.pkl")

print("\n모델 저장 완료!")

print("생성 파일:")
print("- rf_model.pkl")
print("- feature_names.pkl")

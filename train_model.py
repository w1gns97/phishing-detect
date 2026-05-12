import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv("dataset.csv")

target_col = "Result"
X = df.drop(target_col, axis=1)
y = df[target_col]

model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X, y)

joblib.dump(model, "rf_model.pkl")
joblib.dump(list(X.columns), "feature_names.pkl")

print("모델 학습 완료!")

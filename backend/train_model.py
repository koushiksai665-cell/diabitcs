"""
train_model.py
Trains the Random Forest + Gradient Boosting ensemble on the Pima Indians
Diabetes Dataset and saves it as a single .pkl file the Flask API can load.
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
import joblib

# 1. Load dataset directly — no Kaggle login needed, no manual download.
#    Same Pima Indians Diabetes Dataset (768 rows, 8 features), just hosted
#    as a raw CSV with no header row, so we supply column names ourselves.
DATA_URL = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
FEATURES = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
            "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"]
df = pd.read_csv(DATA_URL, header=None, names=FEATURES + ["Outcome"])

X = df[FEATURES]
y = df["Outcome"]

# 2. Clean implausible zeros (median imputation grouped by outcome)
zero_cols = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]
for col in zero_cols:
    X[col] = X[col].replace(0, np.nan)
    X[col] = X.groupby(y)[col].transform(lambda s: s.fillna(s.median()))

# 3. Scale
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, stratify=y, random_state=42
)

# 4. Train ensemble members
rf = RandomForestClassifier(n_estimators=300, max_depth=8, random_state=42)
gb = GradientBoostingClassifier(n_estimators=200, learning_rate=0.05, random_state=42)
rf.fit(X_train, y_train)
gb.fit(X_train, y_train)

rf_acc = rf.score(X_test, y_test)
gb_acc = gb.score(X_test, y_test)
print(f"Random Forest accuracy: {rf_acc:.4f}")
print(f"Gradient Boosting accuracy: {gb_acc:.4f}")

# 5. Bundle everything the API needs into one file
joblib.dump({
    "rf_model": rf,
    "gb_model": gb,
    "scaler": scaler,
    "feature_order": FEATURES,
    "weights": {"rf": 0.55, "gb": 0.45}
}, "diabetes_ensemble.pkl")

print("Saved diabetes_ensemble.pkl")

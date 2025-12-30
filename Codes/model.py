import pandas as pd
import numpy as np

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler, FunctionTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, f1_score, confusion_matrix,
    roc_auc_score, classification_report
)

# =========================
# CONFIG
# =========================
DATA_PATH = "nyc_vehicle_collisions.csv"
TOP_K_VEHICLE_TYPES = 20
RANDOM_STATE = 42
TEST_SIZE = 0.2
N_SPLITS = 5

CLASS_WEIGHTS = [
    {0: 1, 1: 2.0},
    {0: 1, 1: 3.0},
]

C_VALUES = [0.3, 1.0]

PENALTIES = ["l1", "l2"]

THRESHOLDS = [0.35, 0.45, 0.55]


# =========================
# CUSTOM TRANSFORMERS
# =========================
class TopKReducer(BaseEstimator, TransformerMixin):
    def __init__(self, top_k=20):
        self.top_k = top_k
        self.top_categories_ = None

    def fit(self, X, y=None):
        s = X.iloc[:, 0].dropna().astype(str).str.lower().str.strip()
        self.top_categories_ = s.value_counts().nlargest(self.top_k).index
        return self

    def transform(self, X):
        s = X.iloc[:, 0]
        nan_mask = s.isna()
        s = s.astype(str).str.lower().str.strip()
        s = s.where(s.isin(self.top_categories_), "other")
        s[nan_mask] = np.nan
        return s.to_frame()


class VehicleInteractionEncoder(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        v1 = X.iloc[:, 0].fillna("unknown").astype(str).str.lower().str.strip()
        v2 = X.iloc[:, 1].fillna("unknown").astype(str).str.lower().str.strip()
        return (v1 + "_vs_" + v2).to_frame("vehicle_interaction")


def extract_hour(X):
    return pd.to_datetime(
        X["crash_time"], format="%H:%M", errors="coerce"
    ).dt.hour.to_frame("crash_hour")


def extract_temporal_features(X):
    d = pd.to_datetime(X["crash_date"], errors="coerce")
    return pd.DataFrame({
        "day_of_week": d.dt.dayofweek,
        "is_weekend": (d.dt.dayofweek >= 5).astype(int),
        "month": d.dt.month,
        "is_rush_hour": X["crash_time"].apply(
            lambda x: 1 if pd.notna(x) and (
                ("07:00" <= str(x) <= "09:00") or
                ("17:00" <= str(x) <= "19:00")
            ) else 0
        )
    })

# =========================
# LOAD DATA
# =========================
df = pd.read_csv(DATA_PATH)

df["casualty_occurred"] = (
    (df["number_of_persons_injured"] > 0) |
    (df["number_of_persons_killed"] > 0)
).astype(int)

TARGET = "casualty_occurred"

DROP_COLS = [
    "number_of_persons_injured",
    "number_of_persons_killed",
    "number_of_pedestrians_injured",
    "number_of_pedestrians_killed",
    "number_of_cyclist_injured",
    "number_of_cyclist_killed",
    "number_of_motorist_injured",
    "number_of_motorist_killed",
    "collision_id",
    ":id", ":version", ":created_at", ":updated_at",
    "latitude", "longitude",
    "on_street_name", "cross_street_name",
    "off_street_name", "location",
    "contributing_factor_vehicle_1",
    "contributing_factor_vehicle_2",
    "contributing_factor_vehicle_3",
    "contributing_factor_vehicle_4",
    "contributing_factor_vehicle_5",
]

df = df.drop(columns=[c for c in DROP_COLS if c in df.columns])

X = df.drop(columns=[TARGET])
y = df[TARGET].values

# =========================
# TRAIN / TEST SPLIT
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=TEST_SIZE,
    random_state=RANDOM_STATE,
    stratify=y
)

# =========================
# PREPROCESS
# =========================
preprocess = ColumnTransformer(
    transformers=[
        ("time", Pipeline([
            ("h", FunctionTransformer(extract_hour, validate=False)),
            ("imp", SimpleImputer(strategy="median")),
            ("sc", StandardScaler()),
        ]), ["crash_time"]),

        ("temporal", Pipeline([
            ("t", FunctionTransformer(extract_temporal_features, validate=False)),
            ("imp", SimpleImputer(strategy="most_frequent")),
            ("sc", StandardScaler()),
        ]), ["crash_date", "crash_time"]),

        ("veh1", Pipeline([
            ("topk", TopKReducer(TOP_K_VEHICLE_TYPES)),
            ("imp", SimpleImputer(strategy="most_frequent")),
            ("oh", OneHotEncoder(handle_unknown="ignore")),
        ]), ["vehicle_type_code1"]),

        ("veh2", Pipeline([
            ("topk", TopKReducer(TOP_K_VEHICLE_TYPES)),
            ("imp", SimpleImputer(strategy="most_frequent")),
            ("oh", OneHotEncoder(handle_unknown="ignore")),
        ]), ["vehicle_type_code2"]),

        ("veh_inter", Pipeline([
            ("i", VehicleInteractionEncoder()),
            ("topk", TopKReducer(30)),
            ("imp", SimpleImputer(strategy="most_frequent")),
            ("oh", OneHotEncoder(handle_unknown="ignore")),
        ]), ["vehicle_type_code1", "vehicle_type_code2"]),

        ("borough", Pipeline([
            ("imp", SimpleImputer(strategy="most_frequent")),
            ("oh", OneHotEncoder(handle_unknown="ignore")),
        ]), ["borough"]),
    ]
)

# =========================
# CROSS-VALIDATION SEARCH
# =========================
skf = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=RANDOM_STATE)

best_f1 = -1
best_cfg = None

for cw in CLASS_WEIGHTS:
    for C in C_VALUES:
        for pen in PENALTIES:
            solver = "saga" if pen == "l1" else "lbfgs"

            for tr_idx, val_idx in skf.split(X_train, y_train):
                X_tr, X_val = X_train.iloc[tr_idx], X_train.iloc[val_idx]
                y_tr, y_val = y_train[tr_idx], y_train[val_idx]

                pipe = Pipeline([
                    ("prep", preprocess),
                    ("lr", LogisticRegression(
                        penalty=pen,
                        C=C,
                        class_weight=cw,
                        solver=solver,
                        max_iter=400,
                        n_jobs=-1
                    ))
                ])

                pipe.fit(X_tr, y_tr)
                probs = pipe.predict_proba(X_val)[:, 1]

                for t in THRESHOLDS:
                    preds = (probs >= t).astype(int)
                    f1 = f1_score(y_val, preds)

                    if f1 > best_f1:
                        best_f1 = f1
                        best_cfg = {
                            "class_weight": cw,
                            "C": C,
                            "penalty": pen,
                            "threshold": t
                        }

print("\nBEST CV CONFIG")
print(best_cfg)
print("Best CV F1:", round(best_f1, 4))

# =========================
# FINAL TRAIN + TEST
# =========================
final_model = Pipeline([
    ("prep", preprocess),
    ("lr", LogisticRegression(
        penalty=best_cfg["penalty"],
        C=best_cfg["C"],
        class_weight=best_cfg["class_weight"],
        solver="saga" if best_cfg["penalty"] == "l1" else "lbfgs",
        max_iter=500,
        n_jobs=-1
    ))
])

final_model.fit(X_train, y_train)

y_proba = final_model.predict_proba(X_test)[:, 1]
y_pred = (y_proba >= best_cfg["threshold"]).astype(int)

print("\nFINAL TEST PERFORMANCE")
print("Accuracy :", accuracy_score(y_test, y_pred))
print("F1-score :", f1_score(y_test, y_pred))
print("ROC-AUC  :", roc_auc_score(y_test, y_proba))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=["No Casualty", "Casualty"]))

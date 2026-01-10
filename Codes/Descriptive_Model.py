import pandas as pd
import numpy as np
import statsmodels.formula.api as smf

# =========================
# LOAD DATA
# =========================
DATA_PATH = "nyc_vehicle_collisions.csv"
df = pd.read_csv(DATA_PATH)

# =========================
# TARGET: CASUALTY (BINARY)
# =========================
df["casualty"] = (
    (pd.to_numeric(df["number_of_persons_injured"], errors="coerce").fillna(0) > 0) |
    (pd.to_numeric(df["number_of_persons_killed"], errors="coerce").fillna(0) > 0)
).astype(int)

# =========================
# TIME FEATURES
# =========================
df["hour"] = pd.to_datetime(df["crash_time"], format="%H:%M", errors="coerce").dt.hour
d = pd.to_datetime(df["crash_date"], errors="coerce")
df["is_weekend"] = (d.dt.dayofweek >= 5).astype(int)

# =========================
# DROP MISSING
# =========================
df = df.dropna(subset=[
    "casualty",
    "hour",
    "is_weekend",
    "borough",
    "vehicle_type_code1",
    "vehicle_type_code2",
    "contributing_factor_vehicle_1",
    "contributing_factor_vehicle_2"
])

# =========================
# OPTIONAL: TOP-K REDUCTION
# =========================
def topk(series, k=6):
    top = series.value_counts().nlargest(k).index
    return series.where(series.isin(top), "other")

df["vehicle_type_code1"] = topk(df["vehicle_type_code1"], 6)
df["vehicle_type_code2"] = topk(df["vehicle_type_code2"], 6)
df["contributing_factor_vehicle_1"] = topk(df["contributing_factor_vehicle_1"], 6)
df["contributing_factor_vehicle_2"] = topk(df["contributing_factor_vehicle_2"], 6)

# =========================
# LOGISTIC REGRESSION (DESCRIPTIVE)
# =========================
formula = """
casualty ~
hour +
is_weekend +
C(borough) +
C(vehicle_type_code1) +
C(vehicle_type_code2) +
C(contributing_factor_vehicle_1) +
C(contributing_factor_vehicle_2)
"""

model = smf.logit(formula=formula, data=df).fit()

print("\n=== LOGISTIC MODEL SUMMARY ===")
print(model.summary())

# =========================
# ODDS RATIOS + WALD STATS
# =========================
params = model.params
conf = model.conf_int()
conf.columns = ["CI_low", "CI_high"]

or_table = pd.DataFrame({
    "Coefficient": params,
    "Odds_Ratio": np.exp(params),
    "CI_low": np.exp(conf["CI_low"]),
    "CI_high": np.exp(conf["CI_high"]),
    "p_value": model.pvalues
}).sort_values("Odds_Ratio", ascending=False)

print("\n=== ODDS RATIOS (DESCRIPTIVE) ===")
print(or_table.round(4))

or_table.round(6).to_csv("rq3_logistic_odds_ratios.csv")

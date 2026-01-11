import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf

# =========================
# LOAD MERGED DATA
# =========================
DATA_PATH = "nyc_vehicle_collisions_merged2.csv"
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

model = smf.logit(formula=formula, data=df).fit(disp=False)

# =========================
# ODDS RATIOS
# =========================
params = model.params
or_table = pd.DataFrame({
    "odds_ratio": np.exp(params),
    "p_value": model.pvalues
})

or_table = or_table.drop("Intercept")

# =========================
# CLEAN LABELS
# =========================
def clean_label(x):
    x = x.replace("C(", "").replace(")", "").replace("[T.", ": ").replace("]", "")
    x = x.replace("vehicle_type_code1:", "")
    x = x.replace("vehicle_type_code2:", "")
    x = x.replace("contributing_factor_vehicle_1:", "")
    x = x.replace("contributing_factor_vehicle_2:", "")
    return x.strip().title()

or_table["label"] = or_table.index.map(clean_label)

# =========================
# VEHICLE TYPE (MERGED)
# =========================
veh = or_table.loc[or_table.index.str.contains("vehicle_type")]
veh = veh.groupby("label")["odds_ratio"].max().sort_values(ascending=True)

# =========================
# CONTRIBUTING FACTORS
# =========================
fact = or_table.loc[or_table.index.str.contains("contributing_factor")]
fact = fact.groupby("label")["odds_ratio"].max().sort_values(ascending=True)

# =========================
# TIME EFFECTS
# =========================
time = or_table.loc[or_table.index.isin(["hour", "is_weekend"])]
time.index = ["Hour of Day", "Weekend"]
time = time["odds_ratio"]

# =========================
# PLOT
# =========================
fig, axes = plt.subplots(1, 3, figsize=(16, 6))

# --- Vehicle Type (log scale) ---
axes[0].barh(veh.index, veh.values)
axes[0].axvline(1, linestyle="--")
axes[0].set_xscale("log")
axes[0].set_title("Vehicle Type (log scale)")
axes[0].set_xlabel("Odds Ratio")

# --- Contributing Factors ---
axes[1].barh(fact.index, fact.values)
axes[1].axvline(1, linestyle="--")
axes[1].set_title("Contributing Factors")
axes[1].set_xlabel("Odds Ratio")

# --- Time Effects ---
axes[2].barh(time.index, time.values)
axes[2].axvline(1, linestyle="--")
axes[2].set_title("Time Effects")
axes[2].set_xlabel("Odds Ratio")

fig.suptitle(
    "Factors Associated with Casualty Occurrence (Descriptive Logistic Regression)",
    fontsize=14
)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig("rq3_descriptive_logistic_final.png", dpi=300)
plt.close()

print("Saved: rq3_descriptive_logistic_final.png")

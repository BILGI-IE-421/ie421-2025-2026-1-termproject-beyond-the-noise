import pandas as pd
import matplotlib.pyplot as plt

# =========================
# LOAD RESULTS
# =========================
df = pd.read_csv("rq3_logistic_odds_ratios.csv", index_col=0)

# Sadece anlamlılar
df = df[df["p_value"] < 0.05]

# =========================
# VARIABLE GROUPS
# =========================
veh = df[df.index.str.contains("vehicle_type")].head(6)
fac = df[df.index.str.contains("contributing_factor")].head(6)
time = df.loc[["hour", "is_weekend"]]

# =========================
# CLEAN LABELS
# =========================
def clean(name):
    return (
        name.replace("C(", "")
            .replace(")", "")
            .replace("[T.", ": ")
            .replace("_", " ")
    )

veh.index = veh.index.map(clean)
fac.index = fac.index.map(clean)
time.index = ["Hour of Day", "Weekend"]

# =========================
# PLOT
# =========================
fig, axes = plt.subplots(1, 3, figsize=(14, 4))

# --- Panel A: Vehicle Types ---
axes[0].barh(veh.index[::-1], veh["Odds_Ratio"][::-1])
axes[0].axvline(1, linestyle="--")
axes[0].set_title("Vehicle Type")
axes[0].set_xlabel("Odds Ratio")

# --- Panel B: Contributing Factors ---
axes[1].barh(fac.index[::-1], fac["Odds_Ratio"][::-1])
axes[1].axvline(1, linestyle="--")
axes[1].set_title("Contributing Factors")
axes[1].set_xlabel("Odds Ratio")

# --- Panel C: Time ---
axes[2].barh(time.index, time["Odds_Ratio"])
axes[2].axvline(1, linestyle="--")
axes[2].set_title("Time Effects")
axes[2].set_xlabel("Odds Ratio")

fig.suptitle(
    "Factors Associated with Casualty Occurrence (Logistic Regression)",
    fontsize=12
)

plt.tight_layout()
plt.savefig("fig_rq3_descriptive.png", dpi=300)
plt.close()

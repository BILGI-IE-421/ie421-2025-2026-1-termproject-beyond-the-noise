import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("nyc_vehicle_collisions_merged2.csv")

# =========================
# CASUALTY (BINARY)
# =========================
df["casualty"] = (
    (df["number_of_persons_injured"].fillna(0) > 0) |
    (df["number_of_persons_killed"].fillna(0) > 0)
).astype(int)

# =========================
# SELECT MAIN CATEGORIES
# =========================
veh = "vehicle_type_code2"                 # secondary vehicle
fac = "contributing_factor_vehicle_1"      # primary factor

df = df.dropna(subset=[veh, fac])

# =========================
# AGGREGATE: CASUALTY RATE
# =========================
heat_df = (
    df
    .groupby([veh, fac])["casualty"]
    .mean()
    .reset_index()
)

pivot = heat_df.pivot(index=veh, columns=fac, values="casualty")

# =========================
# PLOT HEATMAP
# =========================
plt.figure(figsize=(12, 6))
sns.heatmap(
    pivot,
    cmap="Reds",
    annot=False,
    linewidths=0.5
)

plt.title("Casualty Rate by Vehicle Type and Contributing Factor")
plt.xlabel("Contributing Factor")
plt.ylabel("Vehicle Type")

plt.tight_layout()
plt.savefig("rq3_vehicle_factor_heatmap.png", dpi=300)
plt.close()

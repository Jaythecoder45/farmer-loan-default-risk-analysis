import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/farmer_loans_synthetic.csv")

plt.style.use("default")

# 1. Default rate by crop type
fig, ax = plt.subplots(figsize=(7, 4.2))
rate_by_crop = (
    df.groupby("crop_type")["repayment_status"]
    .apply(lambda x: (x == "Defaulted").mean() * 100)
    .sort_values(ascending=False)
)
bars = ax.bar(rate_by_crop.index, rate_by_crop.values, color="#c0392b")
ax.set_ylabel("Default Rate (%)")
ax.set_title("Default Rate by Crop Type")
for b in bars:
    ax.text(b.get_x() + b.get_width()/2, b.get_height() + 0.4, f"{b.get_height():.1f}%", ha="center", fontsize=9)
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig("charts/default_rate_by_crop.png", dpi=130)
plt.close()

# 2. Default rate by loan-to-land ratio quartile
df["ratio_quartile"] = pd.qcut(df["loan_to_land_ratio"], 4, labels=["Q1 (lowest)", "Q2", "Q3", "Q4 (highest)"])
rate_by_q = df.groupby("ratio_quartile", observed=True)["repayment_status"].apply(lambda x: (x == "Defaulted").mean() * 100)
fig, ax = plt.subplots(figsize=(6.5, 4.2))
bars = ax.bar(rate_by_q.index.astype(str), rate_by_q.values, color="#2874a6")
ax.set_ylabel("Default Rate (%)")
ax.set_title("Default Rate by Loan-to-Land Ratio Quartile")
for b in bars:
    ax.text(b.get_x() + b.get_width()/2, b.get_height() + 0.4, f"{b.get_height():.1f}%", ha="center", fontsize=9)
plt.tight_layout()
plt.savefig("charts/default_rate_by_ratio_quartile.png", dpi=130)
plt.close()

# 3. Season comparison
rate_by_season = df.groupby("season")["repayment_status"].apply(lambda x: (x == "Defaulted").mean() * 100)
fig, ax = plt.subplots(figsize=(5, 4.2))
bars = ax.bar(rate_by_season.index, rate_by_season.values, color=["#e67e22", "#27ae60"])
ax.set_ylabel("Default Rate (%)")
ax.set_title("Default Rate: Kharif vs Rabi Season")
for b in bars:
    ax.text(b.get_x() + b.get_width()/2, b.get_height() + 0.4, f"{b.get_height():.1f}%", ha="center", fontsize=9)
plt.tight_layout()
plt.savefig("charts/default_rate_by_season.png", dpi=130)
plt.close()

# 4. Prior default history
rate_by_hist = df.assign(
    history=lambda d: d["prior_defaults"].gt(0).map({True: "Has prior default", False: "No prior default"})
).groupby("history")["repayment_status"].apply(lambda x: (x == "Defaulted").mean() * 100)
fig, ax = plt.subplots(figsize=(5, 4.2))
bars = ax.bar(rate_by_hist.index, rate_by_hist.values, color=["#8e44ad", "#16a085"])
ax.set_ylabel("Default Rate (%)")
ax.set_title("Default Rate by Prior Repayment History")
for b in bars:
    ax.text(b.get_x() + b.get_width()/2, b.get_height() + 0.4, f"{b.get_height():.1f}%", ha="center", fontsize=9)
plt.tight_layout()
plt.savefig("charts/default_rate_by_history.png", dpi=130)
plt.close()

print("Charts saved to charts/")
print(rate_by_crop)

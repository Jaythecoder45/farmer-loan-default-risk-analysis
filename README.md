# Farmer Loan Default Risk Analysis

## Overview
A risk analysis project on cooperative-society farmer lending, inspired by direct
exposure to loan processing during a Data Entry internship at Mahur Vikas Society.
The dataset is **synthetically generated** (not real society records — those are
confidential) but modeled on realistic patterns: loan-to-land ratios, crop type,
seasonal (Kharif/Rabi) lending cycles, and prior repayment history.

## Objective
Identify which borrower and loan characteristics are associated with higher
default risk, to support early-warning segmentation for a lending institution.

## Tech Stack
- **Python / Pandas** — data generation, cleaning, EDA
- **SQL (sqlite3)** — JOINs, GROUP BY/HAVING, CTEs, Window Functions (NTILE, RANK)
- **Matplotlib** — visualization

## Key Findings
1. **Crop type matters**: Cash/volatile-price crops (Sugarcane 27.6%, Cotton 26.2%)
   showed materially higher default rates than staple crops (Soybean 16.6%, Wheat 18.2%).
2. **Season matters**: Kharif (monsoon-dependent) loans defaulted at 24.9% vs. 17.6%
   for Rabi (irrigated) loans — a ~7 point gap tied to rainfall dependency.
3. **Loan-to-land ratio is the strongest single signal**: the top quartile of
   loan-to-land ratio had a 29.5% default rate vs. ~18-19% in the bottom two quartiles.
4. **Prior default history nearly doubles risk**: borrowers with any prior default
   defaulted at 33.1% vs. 19.5% for clean-history borrowers.
5. **Regional variation**: default rates ranged from 18.9% (Indapur) to 24.1%
   (Baramati) across the five regions studied.


   ```python
import pandas as pd
import matplotlib.pyplot as plt
```


```python
df = pd.read_csv("farmer_loans_synthetic.csv")
```


```python
plt.style.use("default")
```


```python
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
plt.show()
plt.close()
```


    
![png](charts/default_rate_by_crop.png)
    



```python
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
plt.show()
plt.close()
```


    
![png](output_4_0.png)
    



```python
rate_by_season = df.groupby("season")["repayment_status"].apply(lambda x: (x == "Defaulted").mean() * 100)
fig, ax = plt.subplots(figsize=(5, 4.2))
bars = ax.bar(rate_by_season.index, rate_by_season.values, color=["#e67e22", "#27ae60"])
ax.set_ylabel("Default Rate (%)")
ax.set_title("Default Rate: Kharif vs Rabi Season")
for b in bars:
    ax.text(b.get_x() + b.get_width()/2, b.get_height() + 0.4, f"{b.get_height():.1f}%", ha="center", fontsize=9)
plt.tight_layout()
plt.savefig("charts/default_rate_by_season.png", dpi=130)
plt.show()
plt.close()
```


    
![png](output_5_0.png)
    



```python
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
plt.show()
plt.close()

print("Charts saved to charts/")
print(rate_by_crop)
```


    
![png](output_6_0.png)
    


    Charts saved to charts/
    crop_type
    Sugarcane    27.564103
    Cotton       26.181818
    Onion        21.828909
    Jowar        19.611650
    Wheat        18.245614
    Soybean      16.611296
    Name: repayment_status, dtype: float64
    


```python

```


## Files
- `sql_analysis.py` — SQL analysis (JOINs, CTEs, Window Functions)
- `eda_visualize.py` — Python EDA and chart generation
- `data/farmer_loans_synthetic.csv` — the dataset (3,200 records)
- `charts/` — visualizations
- `sql_findings.txt` — raw SQL query outputs



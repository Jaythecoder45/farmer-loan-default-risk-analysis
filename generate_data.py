"""
Generate a synthetic farmer-loan dataset modeled on cooperative credit society
lending patterns (based on domain exposure from a data-entry internship at a
farmer cooperative society). This is SYNTHETIC data for portfolio purposes,
not real society records -- structured to be realistic, not copied from any
real farmer's data.
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
N = 3200

regions = ["Baramati", "Indapur", "Daund", "Phaltan", "Malshiras"]
crop_types = ["Sugarcane", "Cotton", "Soybean", "Wheat", "Jowar", "Onion"]
# crops with higher market-price volatility (cash crops) -> more repayment risk
volatile_crops = {"Sugarcane", "Cotton", "Onion"}
seasons = ["Kharif", "Rabi"]  # Kharif = monsoon-dependent, Rabi = irrigated/winter

farmer_id = np.arange(1, N + 1)
region = rng.choice(regions, N)
land_holding_acres = np.round(rng.gamma(shape=2.2, scale=1.6, size=N) + 0.5, 1)
prior_loan_count = rng.poisson(1.4, N)
prior_defaults = np.where(
    prior_loan_count > 0,
    rng.binomial(prior_loan_count, 0.12),
    0
)

crop_type = rng.choice(crop_types, N, p=[0.20, 0.18, 0.20, 0.17, 0.15, 0.10])
season = rng.choice(seasons, N, p=[0.55, 0.45])

# Loan amount scales loosely with land holding + some noise, in INR
base_loan = land_holding_acres * rng.uniform(8000, 15000, N)
loan_amount = np.round(base_loan * rng.uniform(0.8, 1.3, N), -2).astype(int)
loan_amount = np.clip(loan_amount, 15000, 400000)

interest_rate = np.round(rng.uniform(7.0, 12.0, N), 2)

loan_to_land_ratio = loan_amount / land_holding_acres

# ---- Build a genuine (synthetic) default-risk signal ----
# logistic-style score combining real risk factors, then sample outcome
score = (
    -2.2
    + 0.55 * (loan_to_land_ratio > np.percentile(loan_to_land_ratio, 75))
    + 0.65 * np.isin(crop_type, list(volatile_crops))
    + 0.5 * (season == "Kharif")
    + 0.9 * (prior_defaults > 0)
    - 0.35 * (prior_loan_count >= 2)  # repeat, non-defaulting borrowers are safer
    + rng.normal(0, 0.4, N)
)
prob_default = 1 / (1 + np.exp(-score))
defaulted = rng.binomial(1, prob_default)

# among non-defaulters, some still pay late
paid_late = np.where(
    (defaulted == 0),
    rng.binomial(1, 0.18 + 0.1 * (season == "Kharif")),
    0
)

status = np.select(
    [defaulted == 1, paid_late == 1],
    ["Defaulted", "Paid Late"],
    default="Paid On Time"
)

days_overdue = np.where(
    status == "Paid Late", rng.integers(5, 60, N),
    np.where(status == "Defaulted", rng.integers(90, 400, N), 0)
)

df = pd.DataFrame({
    "loan_id": [f"L{100000+i}" for i in farmer_id],
    "farmer_id": [f"F{20000+i}" for i in farmer_id],
    "region": region,
    "land_holding_acres": land_holding_acres,
    "prior_loan_count": prior_loan_count,
    "prior_defaults": prior_defaults,
    "crop_type": crop_type,
    "season": season,
    "loan_amount": loan_amount,
    "interest_rate": interest_rate,
    "loan_to_land_ratio": np.round(loan_to_land_ratio, 0),
    "repayment_status": status,
    "days_overdue": days_overdue,
})

df.to_csv("data/farmer_loans_synthetic.csv", index=False)
print(df.shape)
print(df["repayment_status"].value_counts(normalize=True).round(3))
print(df.head())

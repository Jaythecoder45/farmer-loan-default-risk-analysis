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

## Files
- `sql_analysis.py` — SQL analysis (JOINs, CTEs, Window Functions)
- `eda_visualize.py` — Python EDA and chart generation
- `data/farmer_loans_synthetic.csv` — the dataset (3,200 records)
- `charts/` — visualizations
- `sql_findings.txt` — raw SQL query outputs



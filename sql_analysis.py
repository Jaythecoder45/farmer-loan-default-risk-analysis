"""
Real SQL analysis on the synthetic farmer loan dataset using sqlite3.
Demonstrates JOINs, GROUP BY/HAVING, CTEs, and Window Functions -- the
exact SQL skills claimed on the resume, run against actual data.
"""
import sqlite3
import pandas as pd

df = pd.read_csv("data/farmer_loans_synthetic.csv")

conn = sqlite3.connect(":memory:")
df.to_sql("loans", conn, index=False, if_exists="replace")

# Split into two related tables to justify a real JOIN
farmers = df[["farmer_id", "region", "land_holding_acres", "prior_loan_count", "prior_defaults"]].drop_duplicates()
loan_details = df[["loan_id", "farmer_id", "crop_type", "season", "loan_amount",
                    "interest_rate", "loan_to_land_ratio", "repayment_status", "days_overdue"]]

farmers.to_sql("farmers", conn, index=False, if_exists="replace")
loan_details.to_sql("loan_details", conn, index=False, if_exists="replace")

print("=" * 70)
print("QUERY 1: Default rate by crop type (JOIN + GROUP BY + HAVING)")
print("=" * 70)
q1 = """
SELECT
    ld.crop_type,
    COUNT(*) AS total_loans,
    ROUND(100.0 * SUM(CASE WHEN ld.repayment_status = 'Defaulted' THEN 1 ELSE 0 END) / COUNT(*), 1) AS default_rate_pct
FROM loan_details ld
JOIN farmers f ON f.farmer_id = ld.farmer_id
GROUP BY ld.crop_type
HAVING COUNT(*) > 50
ORDER BY default_rate_pct DESC
"""
r1 = pd.read_sql(q1, conn)
print(r1.to_string(index=False))

print("\n" + "=" * 70)
print("QUERY 2: Default rate by season (Kharif vs Rabi)")
print("=" * 70)
q2 = """
SELECT season,
       COUNT(*) AS total_loans,
       ROUND(100.0 * SUM(CASE WHEN repayment_status='Defaulted' THEN 1 ELSE 0 END)/COUNT(*),1) AS default_rate_pct
FROM loan_details
GROUP BY season
"""
r2 = pd.read_sql(q2, conn)
print(r2.to_string(index=False))

print("\n" + "=" * 70)
print("QUERY 3: CTE + Window Function - loan-to-land ratio quartile risk")
print("=" * 70)
q3 = """
WITH ranked AS (
    SELECT
        loan_id,
        loan_to_land_ratio,
        repayment_status,
        NTILE(4) OVER (ORDER BY loan_to_land_ratio) AS ratio_quartile
    FROM loan_details
)
SELECT
    ratio_quartile,
    COUNT(*) AS total_loans,
    ROUND(100.0 * SUM(CASE WHEN repayment_status='Defaulted' THEN 1 ELSE 0 END)/COUNT(*),1) AS default_rate_pct
FROM ranked
GROUP BY ratio_quartile
ORDER BY ratio_quartile
"""
r3 = pd.read_sql(q3, conn)
print(r3.to_string(index=False))

print("\n" + "=" * 70)
print("QUERY 4: Prior default history vs new-loan default rate")
print("=" * 70)
q4 = """
SELECT
    CASE WHEN f.prior_defaults > 0 THEN 'Has prior default' ELSE 'No prior default' END AS borrower_history,
    COUNT(*) AS total_loans,
    ROUND(100.0 * SUM(CASE WHEN ld.repayment_status='Defaulted' THEN 1 ELSE 0 END)/COUNT(*),1) AS default_rate_pct
FROM loan_details ld
JOIN farmers f ON f.farmer_id = ld.farmer_id
GROUP BY borrower_history
"""
r4 = pd.read_sql(q4, conn)
print(r4.to_string(index=False))

print("\n" + "=" * 70)
print("QUERY 5: Region-wise ranking of default rate (Window Function - RANK)")
print("=" * 70)
q5 = """
WITH region_stats AS (
    SELECT
        f.region,
        COUNT(*) AS total_loans,
        ROUND(100.0 * SUM(CASE WHEN ld.repayment_status='Defaulted' THEN 1 ELSE 0 END)/COUNT(*),1) AS default_rate_pct
    FROM loan_details ld
    JOIN farmers f ON f.farmer_id = ld.farmer_id
    GROUP BY f.region
)
SELECT *, RANK() OVER (ORDER BY default_rate_pct DESC) AS risk_rank
FROM region_stats
"""
r5 = pd.read_sql(q5, conn)
print(r5.to_string(index=False))

# save results for README
with open("sql_findings.txt", "w") as f:
    f.write("CROP TYPE:\n" + r1.to_string(index=False) + "\n\n")
    f.write("SEASON:\n" + r2.to_string(index=False) + "\n\n")
    f.write("LOAN-TO-LAND RATIO QUARTILE:\n" + r3.to_string(index=False) + "\n\n")
    f.write("PRIOR DEFAULT HISTORY:\n" + r4.to_string(index=False) + "\n\n")
    f.write("REGION RANKING:\n" + r5.to_string(index=False) + "\n")

conn.close()

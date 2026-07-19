SELECT * FROM loan_default.fl;


SELECT
    fl.crop_type,
    COUNT(*) AS total_loans,
    ROUND(100.0 * SUM(CASE WHEN fl.repayment_status = 'Defaulted' THEN 1 ELSE 0 END) / COUNT(*), 1) AS default_rate_pct
FROM fl
JOIN fl f ON f.farmer_id = fl.farmer_id
GROUP BY fl.crop_type
HAVING COUNT(*) > 50
ORDER BY default_rate_pct DESC;



SELECT season,
       COUNT(*) AS total_loans,
       ROUND(100.0 * SUM(CASE WHEN repayment_status='Defaulted' THEN 1 ELSE 0 END)/COUNT(*),1) AS default_rate_pct
FROM fl
GROUP BY season;

WITH ranked AS (
    SELECT
        loan_id,
        loan_to_land_ratio,
        repayment_status,
        NTILE(4) OVER (ORDER BY loan_to_land_ratio) AS ratio_quartile
    FROM fl
)
SELECT
    ratio_quartile,
    COUNT(*) AS total_loans,
    ROUND(100.0 * SUM(CASE WHEN repayment_status='Defaulted' THEN 1 ELSE 0 END)/COUNT(*),1) AS default_rate_pct
FROM ranked
GROUP BY ratio_quartile
ORDER BY ratio_quartile;



SELECT
    CASE WHEN f.prior_defaults > 0 THEN 'Has prior default' ELSE 'No prior default' END AS borrower_history,
    COUNT(*) AS total_loans,
    ROUND(100.0 * SUM(CASE WHEN fl.repayment_status='Defaulted' THEN 1 ELSE 0 END)/COUNT(*),1) AS default_rate_pct
FROM fl
JOIN fl f ON f.farmer_id = fl.farmer_id
GROUP BY borrower_history;



WITH region_stats AS (
    SELECT
        f.region,
        COUNT(*) AS total_loans,
        ROUND(100.0 * SUM(CASE WHEN fl.repayment_status='Defaulted' THEN 1 ELSE 0 END)/COUNT(*),1) AS default_rate_pct
    FROM fl
    JOIN fl f ON f.farmer_id = fl.farmer_id
    GROUP BY f.region
)
SELECT *, RANK() OVER (ORDER BY default_rate_pct DESC) AS risk_rank
FROM region_stats;

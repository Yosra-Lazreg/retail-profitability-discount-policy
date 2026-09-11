-- Retail Profitability & Discount Policy
-- Run against a table named orders with the Sample Superstore columns.

WITH banded AS (
  SELECT
    "Sub-Category" AS sub_category,
    CASE
      WHEN "Discount" = 0 THEN '0%'
      WHEN "Discount" <= 0.20 THEN '1-20%'
      WHEN "Discount" <= 0.30 THEN '21-30%'
      WHEN "Discount" <= 0.40 THEN '31-40%'
      ELSE '40%+'
    END AS discount_band,
    "Sales" AS sales,
    "Profit" AS profit
  FROM orders
)
SELECT
  sub_category,
  discount_band,
  COUNT(*) AS order_lines,
  ROUND(SUM(sales)::numeric, 2) AS sales,
  ROUND(SUM(profit)::numeric, 2) AS profit,
  ROUND((100 * SUM(profit) / NULLIF(SUM(sales), 0))::numeric, 2) AS margin_pct
FROM banded
GROUP BY sub_category, discount_band
ORDER BY profit;

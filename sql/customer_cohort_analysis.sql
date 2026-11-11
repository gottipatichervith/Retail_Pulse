
-- ============================================================
-- RETAILPULSE - ADVANCED PHASE WEEK 1
-- TASK 2: CUSTOMER COHORT & RETENTION ANALYSIS
-- Database: SQLite
-- ============================================================

-- Remove previous versions of the views.

DROP VIEW IF EXISTS v_bi_customer_cohort_retention;
DROP VIEW IF EXISTS v_bi_customer_cohort_sizes;
DROP VIEW IF EXISTS v_bi_customer_first_purchase;
DROP VIEW IF EXISTS v_bi_customer_monthly_activity;
DROP VIEW IF EXISTS v_bi_customer_repeat_summary;


-- ============================================================
-- 1. CUSTOMER MONTHLY ACTIVITY
-- Count unique orders placed by each customer in each month.
-- ============================================================

CREATE VIEW v_bi_customer_monthly_activity AS

SELECT
    customer_id,
    strftime('%Y-%m', order_date) AS activity_month,
    COUNT(DISTINCT order_id) AS orders_in_month

FROM v_bi_sales_base

GROUP BY
    customer_id,
    strftime('%Y-%m', order_date);


-- ============================================================
-- 2. CUSTOMER FIRST PURCHASE
-- Identify the month in which each customer first purchased.
-- This month becomes the customer's cohort month.
-- ============================================================

CREATE VIEW v_bi_customer_first_purchase AS

SELECT
    customer_id,
    MIN(activity_month) AS cohort_month

FROM v_bi_customer_monthly_activity

GROUP BY customer_id;


-- ============================================================
-- 3. COHORT SIZES
-- Count how many customers belong to each cohort.
-- ============================================================

CREATE VIEW v_bi_customer_cohort_sizes AS

SELECT
    cohort_month,
    COUNT(DISTINCT customer_id) AS cohort_size

FROM v_bi_customer_first_purchase

GROUP BY cohort_month;


-- ============================================================
-- 4. CUSTOMER REPEAT PURCHASE SUMMARY
-- Identify customers who placed more than one unique order
-- during the complete analysis period.
-- ============================================================

CREATE VIEW v_bi_customer_repeat_summary AS

SELECT
    customer_id,
    COUNT(DISTINCT order_id) AS total_orders,

    CASE
        WHEN COUNT(DISTINCT order_id) > 1 THEN 'Repeat Customer'
        ELSE 'One-Time Customer'
    END AS customer_type

FROM v_bi_sales_base

GROUP BY customer_id;


-- ============================================================
-- 5. COHORT RETENTION ANALYSIS
--
-- Month 0 = First purchase month.
-- Month 1 = Following month.
-- Month 2 = Second month after first purchase.
--
-- Retention measures customers who made at least one
-- purchase in that month.
--
-- Repeat purchase customers are shown separately.
-- ============================================================

CREATE VIEW v_bi_customer_cohort_retention AS

WITH RECURSIVE

-- Generate all months between the first and last purchase.

calendar(activity_month) AS (

    SELECT MIN(activity_month)
    FROM v_bi_customer_monthly_activity

    UNION ALL

    SELECT
        strftime(
            '%Y-%m',
            date(activity_month || '-01', '+1 month')
        )

    FROM calendar

    WHERE activity_month < (
        SELECT MAX(activity_month)
        FROM v_bi_customer_monthly_activity
    )
),

-- Combine every cohort with its possible activity months.

cohort_calendar AS (

    SELECT
        cs.cohort_month,
        calendar.activity_month,
        cs.cohort_size

    FROM v_bi_customer_cohort_sizes cs

    CROSS JOIN calendar

    WHERE calendar.activity_month >= cs.cohort_month
),

-- Calculate customer activity for each cohort and month.

cohort_activity AS (

    SELECT
        cc.cohort_month,
        cc.activity_month,
        cc.cohort_size,

        COUNT(DISTINCT a.customer_id) AS active_customers,

        COUNT(
            DISTINCT CASE
                WHEN a.orders_in_month > 1
                THEN a.customer_id
            END
        ) AS customers_with_multiple_orders_in_month

    FROM cohort_calendar cc

    LEFT JOIN v_bi_customer_first_purchase fp
        ON cc.cohort_month = fp.cohort_month

    LEFT JOIN v_bi_customer_monthly_activity a
        ON fp.customer_id = a.customer_id
        AND cc.activity_month = a.activity_month

    GROUP BY
        cc.cohort_month,
        cc.activity_month,
        cc.cohort_size
)

SELECT

    cohort_month,

    activity_month,

    (
        (CAST(SUBSTR(activity_month, 1, 4) AS INTEGER)
         - CAST(SUBSTR(cohort_month, 1, 4) AS INTEGER)) * 12

        +

        (CAST(SUBSTR(activity_month, 6, 2) AS INTEGER)
         - CAST(SUBSTR(cohort_month, 6, 2) AS INTEGER))
    ) AS month_number,

    cohort_size,

    active_customers,

    ROUND(
        active_customers * 100.0
        / NULLIF(cohort_size, 0),
        2
    ) AS retention_rate_pct,

    customers_with_multiple_orders_in_month

FROM cohort_activity;


-- ============================================================
-- 6. VIEW THE RESULTS
-- ============================================================

-- First purchase month of every customer.

SELECT *
FROM v_bi_customer_first_purchase
ORDER BY cohort_month, customer_id;


-- Number of customers in each cohort.

SELECT *
FROM v_bi_customer_cohort_sizes
ORDER BY cohort_month;


-- Monthly cohort retention results.

SELECT *
FROM v_bi_customer_cohort_retention
ORDER BY cohort_month, month_number;


-- One-time and repeat customer summary.

SELECT
    customer_type,
    COUNT(*) AS customer_count
FROM v_bi_customer_repeat_summary
GROUP BY customer_type;

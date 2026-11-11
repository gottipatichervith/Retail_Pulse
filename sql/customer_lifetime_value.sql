
-- ============================================================
-- RETAILPULSE - ADVANCED PHASE WEEK 1
-- TASK 3: CUSTOMER LIFETIME VALUE (CLV)
-- Database: SQLite
-- ============================================================

DROP VIEW IF EXISTS v_bi_customer_lifetime_value;
DROP VIEW IF EXISTS v_bi_customer_value_segments;
DROP VIEW IF EXISTS v_bi_store_customer_value;


-- ============================================================
-- 1. CUSTOMER LIFETIME VALUE
-- Calculate each customer's historical purchase value.
-- ============================================================

CREATE VIEW v_bi_customer_lifetime_value AS

SELECT

    customer_id,

    ROUND(SUM(net_amount), 2) AS total_spending,

    COUNT(DISTINCT order_id) AS total_orders,

    SUM(quantity) AS total_units_purchased,

    ROUND(
        SUM(net_amount) * 1.0
        / NULLIF(COUNT(DISTINCT order_id), 0),
        2
    ) AS average_order_value,

    MIN(order_date) AS first_purchase_date,

    MAX(order_date) AS last_purchase_date,

    COUNT(DISTINCT strftime('%Y-%m', order_date))
        AS active_purchase_months

FROM v_bi_sales_base

GROUP BY customer_id;


-- ============================================================
-- 2. CUSTOMER VALUE SEGMENTS
-- Divide customers into four groups based on spending.
-- NTILE(4) creates four approximately equal-sized groups.
-- ============================================================

CREATE VIEW v_bi_customer_value_segments AS

WITH customer_ranking AS (

    SELECT

        customer_id,

        total_spending,

        total_orders,

        average_order_value,

        NTILE(4) OVER (
            ORDER BY total_spending DESC, customer_id
        ) AS spending_group

    FROM v_bi_customer_lifetime_value

)

SELECT

    customer_id,

    total_spending,

    total_orders,

    average_order_value,

    spending_group,

    CASE
        WHEN spending_group = 1 THEN 'High Value'
        WHEN spending_group = 2 THEN 'Upper-Middle Value'
        WHEN spending_group = 3 THEN 'Lower-Middle Value'
        ELSE 'Low Value'
    END AS customer_segment

FROM customer_ranking;


-- ============================================================
-- 3. STORE-WISE CUSTOMER VALUE
-- Compare customer spending and order value by store.
-- ============================================================

CREATE VIEW v_bi_store_customer_value AS

SELECT

    store_id,

    COUNT(DISTINCT customer_id) AS customer_count,

    COUNT(DISTINCT order_id) AS total_orders,

    ROUND(SUM(net_amount), 2) AS total_net_sales,

    ROUND(
        SUM(net_amount) * 1.0
        / NULLIF(COUNT(DISTINCT customer_id), 0),
        2
    ) AS average_customer_spending,

    ROUND(
        SUM(net_amount) * 1.0
        / NULLIF(COUNT(DISTINCT order_id), 0),
        2
    ) AS average_order_value

FROM v_bi_sales_base

GROUP BY store_id;


-- ============================================================
-- 4. TOP 10 CUSTOMERS
-- Rank customers based on historical total spending.
-- ============================================================

SELECT

    customer_id,

    total_spending,

    total_orders,

    total_units_purchased,

    average_order_value,

    first_purchase_date,

    last_purchase_date

FROM v_bi_customer_lifetime_value

ORDER BY
    total_spending DESC,
    customer_id

LIMIT 10;


-- ============================================================
-- 5. CUSTOMER VALUE SEGMENT SUMMARY
-- Understand how much each spending group contributes.
-- ============================================================

SELECT

    customer_segment,

    COUNT(*) AS customer_count,

    ROUND(SUM(total_spending), 2) AS total_customer_spending,

    ROUND(
        AVG(total_spending),
        2
    ) AS average_customer_spending,

    ROUND(
        AVG(average_order_value),
        2
    ) AS average_order_value

FROM v_bi_customer_value_segments

GROUP BY
    spending_group,
    customer_segment

ORDER BY spending_group;


-- ============================================================
-- 6. STORE-WISE CUSTOMER VALUE
-- ============================================================

SELECT *

FROM v_bi_store_customer_value

ORDER BY total_net_sales DESC;


-- ============================================================
-- 7. VALIDATION
-- Check the number of customers included in CLV analysis.
-- ============================================================

SELECT

    COUNT(*) AS analyzed_customers,

    ROUND(SUM(total_spending), 2) AS total_customer_spending

FROM v_bi_customer_lifetime_value;

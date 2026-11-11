
-- ============================================================
-- RETAILPULSE - ADVANCED PHASE WEEK 1
-- TASK 1: REUSABLE KPI LAYER
-- Database: SQLite
-- ============================================================

-- Remove old versions of these views if they already exist.

DROP VIEW IF EXISTS v_bi_kpi_overall;
DROP VIEW IF EXISTS v_bi_kpi_monthly;
DROP VIEW IF EXISTS v_bi_kpi_store;
DROP VIEW IF EXISTS v_bi_kpi_product;
DROP VIEW IF EXISTS v_bi_customer_order_counts;
DROP VIEW IF EXISTS v_bi_customer_store_order_counts;
DROP VIEW IF EXISTS v_bi_customer_product_order_counts;
DROP VIEW IF EXISTS v_bi_sales_base;


-- ============================================================
-- 1. BASE SALES VIEW
-- Combines orders and order_items.
-- Excludes the known test order ORD9999.
-- Removes exact duplicate order-item rows.
-- ============================================================

CREATE VIEW v_bi_sales_base AS

WITH ranked_items AS (

    SELECT
        oi.order_id,
        oi.product_id,
        oi.quantity,
        oi.unit_price,
        oi.discount,
        oi.gross_amount,
        oi.net_amount,

        ROW_NUMBER() OVER (
            PARTITION BY
                oi.order_id,
                oi.product_id,
                oi.quantity,
                oi.unit_price,
                oi.discount,
                oi.gross_amount,
                oi.net_amount
            ORDER BY oi.rowid
        ) AS row_num

    FROM order_items oi

)

SELECT
    o.order_id,
    o.order_date,
    o.customer_id,
    o.store_id,
    ri.product_id,
    ri.quantity,
    ri.unit_price,
    ri.discount,
    ri.gross_amount,
    ri.net_amount

FROM orders o

JOIN ranked_items ri
    ON o.order_id = ri.order_id

WHERE
    o.status = 'Completed'
    AND o.order_id <> 'ORD9999'
    AND ri.row_num = 1;


-- ============================================================
-- 2. CUSTOMER ORDER COUNTS
-- Finds how many unique orders each customer placed.
-- ============================================================

CREATE VIEW v_bi_customer_order_counts AS

SELECT
    customer_id,
    COUNT(DISTINCT order_id) AS order_count

FROM v_bi_sales_base

GROUP BY customer_id;


-- ============================================================
-- 3. CUSTOMER ORDER COUNTS BY STORE
-- Used to calculate store-wise repeat purchase rate.
-- ============================================================

CREATE VIEW v_bi_customer_store_order_counts AS

SELECT
    customer_id,
    store_id,
    COUNT(DISTINCT order_id) AS order_count

FROM v_bi_sales_base

GROUP BY
    customer_id,
    store_id;


-- ============================================================
-- 4. CUSTOMER ORDER COUNTS BY PRODUCT
-- Used to calculate product-wise repeat purchase rate.
-- ============================================================

CREATE VIEW v_bi_customer_product_order_counts AS

SELECT
    customer_id,
    product_id,
    COUNT(DISTINCT order_id) AS order_count

FROM v_bi_sales_base

GROUP BY
    customer_id,
    product_id;


-- ============================================================
-- 5. OVERALL BUSINESS KPIs
-- ============================================================

CREATE VIEW v_bi_kpi_overall AS

SELECT

    ROUND(SUM(net_amount), 2) AS total_net_sales,

    COUNT(DISTINCT order_id) AS order_count,

    ROUND(
        SUM(net_amount) * 1.0
        / NULLIF(COUNT(DISTINCT order_id), 0),
        2
    ) AS average_order_value,

    COUNT(DISTINCT customer_id) AS customer_count,

    ROUND(
        (
            SELECT COUNT(*)
            FROM v_bi_customer_order_counts
            WHERE order_count > 1
        ) * 100.0
        / NULLIF(COUNT(DISTINCT customer_id), 0),
        2
    ) AS repeat_purchase_rate_pct

FROM v_bi_sales_base;


-- ============================================================
-- 6. MONTHLY BUSINESS KPIs
-- ============================================================

CREATE VIEW v_bi_kpi_monthly AS

SELECT

    strftime('%Y-%m', b.order_date) AS sales_month,

    ROUND(SUM(b.net_amount), 2) AS total_net_sales,

    COUNT(DISTINCT b.order_id) AS order_count,

    ROUND(
        SUM(b.net_amount) * 1.0
        / NULLIF(COUNT(DISTINCT b.order_id), 0),
        2
    ) AS average_order_value,

    COUNT(DISTINCT b.customer_id) AS customer_count,

    ROUND(
        COUNT(DISTINCT
            CASE
                WHEN c.order_count > 1 THEN b.customer_id
            END
        ) * 100.0
        / NULLIF(COUNT(DISTINCT b.customer_id), 0),
        2
    ) AS repeat_purchase_rate_pct

FROM v_bi_sales_base b

LEFT JOIN v_bi_customer_order_counts c
    ON b.customer_id = c.customer_id

GROUP BY strftime('%Y-%m', b.order_date);


-- ============================================================
-- 7. STORE-WISE BUSINESS KPIs
-- ============================================================

CREATE VIEW v_bi_kpi_store AS

SELECT

    b.store_id,

    ROUND(SUM(b.net_amount), 2) AS total_net_sales,

    COUNT(DISTINCT b.order_id) AS order_count,

    ROUND(
        SUM(b.net_amount) * 1.0
        / NULLIF(COUNT(DISTINCT b.order_id), 0),
        2
    ) AS average_order_value,

    COUNT(DISTINCT b.customer_id) AS customer_count,

    ROUND(
        COUNT(DISTINCT
            CASE
                WHEN c.order_count > 1 THEN b.customer_id
            END
        ) * 100.0
        / NULLIF(COUNT(DISTINCT b.customer_id), 0),
        2
    ) AS repeat_purchase_rate_pct

FROM v_bi_sales_base b

LEFT JOIN v_bi_customer_store_order_counts c
    ON b.customer_id = c.customer_id
    AND b.store_id = c.store_id

GROUP BY b.store_id;


-- ============================================================
-- 8. PRODUCT-WISE BUSINESS KPIs
-- ============================================================

CREATE VIEW v_bi_kpi_product AS

SELECT

    b.product_id,

    ROUND(SUM(b.net_amount), 2) AS total_net_sales,

    COUNT(DISTINCT b.order_id) AS order_count,

    ROUND(
        SUM(b.net_amount) * 1.0
        / NULLIF(COUNT(DISTINCT b.order_id), 0),
        2
    ) AS average_order_value,

    COUNT(DISTINCT b.customer_id) AS customer_count,

    ROUND(
        COUNT(DISTINCT
            CASE
                WHEN c.order_count > 1 THEN b.customer_id
            END
        ) * 100.0
        / NULLIF(COUNT(DISTINCT b.customer_id), 0),
        2
    ) AS repeat_purchase_rate_pct

FROM v_bi_sales_base b

LEFT JOIN v_bi_customer_product_order_counts c
    ON b.customer_id = c.customer_id
    AND b.product_id = c.product_id

GROUP BY b.product_id;


-- ============================================================
-- 9. CHECK THE RESULTS
-- Run these queries to see the KPI results.
-- ============================================================

SELECT * FROM v_bi_kpi_overall;

SELECT * FROM v_bi_kpi_monthly
ORDER BY sales_month;

SELECT * FROM v_bi_kpi_store
ORDER BY store_id;

SELECT * FROM v_bi_kpi_product
ORDER BY product_id;

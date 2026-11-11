
-- ============================================================
-- RETAILPULSE - ADVANCED PHASE WEEK 1
-- TASK 4: PRODUCT & STORE PERFORMANCE
-- Database: SQLite
-- ============================================================

DROP VIEW IF EXISTS v_bi_product_monthly_sales;
DROP VIEW IF EXISTS v_bi_product_mom_growth;
DROP VIEW IF EXISTS v_bi_product_sales_contribution;
DROP VIEW IF EXISTS v_bi_product_store_performance;
DROP VIEW IF EXISTS v_bi_declining_products;


-- ============================================================
-- 1. PRODUCT MONTHLY SALES
-- Calculate product sales for every month.
-- Include months with zero sales.
-- ============================================================

CREATE VIEW v_bi_product_monthly_sales AS

WITH RECURSIVE

calendar(sales_month) AS (

    SELECT MIN(strftime('%Y-%m', order_date))
    FROM v_bi_sales_base

    UNION ALL

    SELECT strftime(
        '%Y-%m',
        date(sales_month || '-01', '+1 month')
    )
    FROM calendar

    WHERE sales_month < (
        SELECT MAX(strftime('%Y-%m', order_date))
        FROM v_bi_sales_base
    )
),

products AS (

    SELECT DISTINCT product_id
    FROM v_bi_sales_base

),

monthly_sales AS (

    SELECT
        product_id,
        strftime('%Y-%m', order_date) AS sales_month,
        SUM(net_amount) AS net_sales,
        SUM(quantity) AS units_sold,
        COUNT(DISTINCT order_id) AS order_count

    FROM v_bi_sales_base

    GROUP BY
        product_id,
        strftime('%Y-%m', order_date)

)

SELECT

    p.product_id,
    c.sales_month,

    COALESCE(m.net_sales, 0) AS net_sales,

    COALESCE(m.units_sold, 0) AS units_sold,

    COALESCE(m.order_count, 0) AS order_count

FROM products p

CROSS JOIN calendar c

LEFT JOIN monthly_sales m
    ON p.product_id = m.product_id
    AND c.sales_month = m.sales_month;


-- ============================================================
-- 2. MONTH-OVER-MONTH PRODUCT GROWTH
-- Compare current month sales with previous month sales.
-- ============================================================

CREATE VIEW v_bi_product_mom_growth AS

WITH previous_sales AS (

    SELECT

        product_id,
        sales_month,
        net_sales,

        LAG(net_sales) OVER (
            PARTITION BY product_id
            ORDER BY sales_month
        ) AS previous_month_sales

    FROM v_bi_product_monthly_sales

)

SELECT

    product_id,
    sales_month,
    net_sales,
    previous_month_sales,

    ROUND(
        net_sales - previous_month_sales,
        2
    ) AS sales_difference,

    ROUND(
        (
            net_sales - previous_month_sales
        ) * 100.0
        / NULLIF(previous_month_sales, 0),
        2
    ) AS mom_growth_pct

FROM previous_sales;


-- ============================================================
-- 3. PRODUCT SALES CONTRIBUTION
-- Calculate each product's share of total net sales.
-- ============================================================

CREATE VIEW v_bi_product_sales_contribution AS

SELECT

    product_id,

    ROUND(SUM(net_amount), 2) AS product_net_sales,

    ROUND(
        SUM(net_amount) * 100.0
        / NULLIF(
            (SELECT SUM(net_amount)
             FROM v_bi_sales_base),
            0
        ),
        2
    ) AS sales_contribution_pct

FROM v_bi_sales_base

GROUP BY product_id;


-- ============================================================
-- 4. PRODUCT PERFORMANCE BY STORE
-- Compare products across different stores.
-- ============================================================

CREATE VIEW v_bi_product_store_performance AS

SELECT

    store_id,
    product_id,

    ROUND(SUM(net_amount), 2) AS net_sales,

    SUM(quantity) AS units_sold,

    COUNT(DISTINCT order_id) AS order_count,

    RANK() OVER (
        PARTITION BY store_id
        ORDER BY SUM(net_amount) DESC
    ) AS product_sales_rank

FROM v_bi_sales_base

GROUP BY
    store_id,
    product_id;


-- ============================================================
-- 5. PRODUCTS DECLINING FOR TWO CONSECUTIVE MONTHLY PERIODS
--
-- Requires at least three months:
-- Month 1 > Month 2 > Month 3.
-- Zero-sales months are included.
-- ============================================================

CREATE VIEW v_bi_declining_products AS

WITH sales_trend AS (

    SELECT

        product_id,
        sales_month,
        net_sales,

        LAG(net_sales, 1) OVER (
            PARTITION BY product_id
            ORDER BY sales_month
        ) AS previous_month_sales,

        LAG(net_sales, 2) OVER (
            PARTITION BY product_id
            ORDER BY sales_month
        ) AS two_months_ago_sales,

        LAG(sales_month, 1) OVER (
            PARTITION BY product_id
            ORDER BY sales_month
        ) AS previous_month,

        LAG(sales_month, 2) OVER (
            PARTITION BY product_id
            ORDER BY sales_month
        ) AS two_months_ago

    FROM v_bi_product_monthly_sales

)

SELECT

    product_id,

    two_months_ago AS first_month,
    previous_month AS second_month,
    sales_month AS third_month,

    two_months_ago_sales AS first_month_sales,
    previous_month_sales AS second_month_sales,
    net_sales AS third_month_sales

FROM sales_trend

WHERE
    two_months_ago_sales IS NOT NULL
    AND previous_month_sales IS NOT NULL

    AND date(previous_month || '-01') =
        date(two_months_ago || '-01', '+1 month')

    AND date(sales_month || '-01') =
        date(previous_month || '-01', '+1 month')

    AND two_months_ago_sales > previous_month_sales
    AND previous_month_sales > net_sales;


-- ============================================================
-- 6. VIEW THE RESULTS
-- ============================================================

-- A. Monthly sales for every product.

SELECT *
FROM v_bi_product_monthly_sales
ORDER BY product_id, sales_month;


-- B. Month-over-month growth.

SELECT *
FROM v_bi_product_mom_growth
ORDER BY product_id, sales_month;


-- C. Product sales contribution.

SELECT *
FROM v_bi_product_sales_contribution
ORDER BY sales_contribution_pct DESC;


-- D. Product performance by store.

SELECT *
FROM v_bi_product_store_performance
ORDER BY store_id, product_sales_rank, product_id;


-- E. Products declining for two consecutive months.

SELECT *
FROM v_bi_declining_products
ORDER BY product_id;

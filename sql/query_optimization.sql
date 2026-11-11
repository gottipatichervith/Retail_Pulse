
-- ============================================================
-- RetailPulse Advanced Phase - Task 5
-- Query Optimization
-- Database: SQLite
--
-- IMPORTANT:
-- Run Task 1's advanced_kpi_layer.sql first.
-- This script uses the v_bi_sales_base view.
-- ============================================================


-- ============================================================
-- PART 1: BASELINE QUERY PLANS
-- Run these before creating the new indexes.
-- ============================================================


-- QUERY 1: Monthly sales

EXPLAIN QUERY PLAN
SELECT
    substr(order_date, 1, 7) AS sales_month,
    SUM(net_amount) AS total_net_sales,
    COUNT(DISTINCT order_id) AS total_orders
FROM v_bi_sales_base
GROUP BY substr(order_date, 1, 7)
ORDER BY sales_month;


-- QUERY 2: Store-wise sales

EXPLAIN QUERY PLAN
SELECT
    store_id,
    SUM(net_amount) AS total_net_sales,
    COUNT(DISTINCT order_id) AS total_orders
FROM v_bi_sales_base
GROUP BY store_id
ORDER BY total_net_sales DESC;


-- QUERY 3: Customer spending

EXPLAIN QUERY PLAN
SELECT
    customer_id,
    SUM(net_amount) AS total_spending,
    COUNT(DISTINCT order_id) AS total_orders
FROM v_bi_sales_base
GROUP BY customer_id
ORDER BY total_spending DESC;


-- QUERY 4: Product performance

EXPLAIN QUERY PLAN
SELECT
    product_id,
    SUM(quantity) AS total_units_sold,
    SUM(net_amount) AS total_net_sales
FROM v_bi_sales_base
GROUP BY product_id
ORDER BY total_net_sales DESC;


-- QUERY 5: Product performance by store

EXPLAIN QUERY PLAN
SELECT
    store_id,
    product_id,
    SUM(net_amount) AS total_net_sales,
    SUM(quantity) AS total_units_sold
FROM v_bi_sales_base
GROUP BY store_id, product_id
ORDER BY store_id, total_net_sales DESC;


-- ============================================================
-- PART 2: CREATE INDEXES
-- Indexes can help SQLite locate and join records efficiently.
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_orders_status_date
ON orders(status, order_date);

CREATE INDEX IF NOT EXISTS idx_orders_customer_status
ON orders(customer_id, status);

CREATE INDEX IF NOT EXISTS idx_orders_store_status
ON orders(store_id, status);

CREATE INDEX IF NOT EXISTS idx_order_items_order_product
ON order_items(order_id, product_id);

CREATE INDEX IF NOT EXISTS idx_order_items_product
ON order_items(product_id);


-- Update SQLite's statistics so its query planner can make
-- better decisions using the available indexes.

ANALYZE;


-- ============================================================
-- PART 3: OPTIMIZED QUERY PLANS
-- Run the same query plans again after creating indexes.
-- Compare these plans with PART 1.
-- ============================================================


-- QUERY 1: Monthly sales

EXPLAIN QUERY PLAN
SELECT
    substr(order_date, 1, 7) AS sales_month,
    SUM(net_amount) AS total_net_sales,
    COUNT(DISTINCT order_id) AS total_orders
FROM v_bi_sales_base
GROUP BY substr(order_date, 1, 7)
ORDER BY sales_month;


-- QUERY 2: Store-wise sales

EXPLAIN QUERY PLAN
SELECT
    store_id,
    SUM(net_amount) AS total_net_sales,
    COUNT(DISTINCT order_id) AS total_orders
FROM v_bi_sales_base
GROUP BY store_id
ORDER BY total_net_sales DESC;


-- QUERY 3: Customer spending

EXPLAIN QUERY PLAN
SELECT
    customer_id,
    SUM(net_amount) AS total_spending,
    COUNT(DISTINCT order_id) AS total_orders
FROM v_bi_sales_base
GROUP BY customer_id
ORDER BY total_spending DESC;


-- QUERY 4: Product performance

EXPLAIN QUERY PLAN
SELECT
    product_id,
    SUM(quantity) AS total_units_sold,
    SUM(net_amount) AS total_net_sales
FROM v_bi_sales_base
GROUP BY product_id
ORDER BY total_net_sales DESC;


-- QUERY 5: Product performance by store

EXPLAIN QUERY PLAN
SELECT
    store_id,
    product_id,
    SUM(net_amount) AS total_net_sales,
    SUM(quantity) AS total_units_sold
FROM v_bi_sales_base
GROUP BY store_id, product_id
ORDER BY store_id, total_net_sales DESC;


-- ============================================================
-- PART 4: VALIDATE INDEXES
-- Displays the indexes created on the main tables.
-- ============================================================

PRAGMA index_list('orders');

PRAGMA index_list('order_items');

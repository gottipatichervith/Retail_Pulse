SELECT COUNT(*) AS total_orders
FROM orders;

SELECT SUM(quantity) AS total_units_sold
FROM order_items;

SELECT SUM(gross_amount) AS total_gross_sales
FROM order_items;

SELECT SUM(discount) AS total_discount
FROM order_items;

SELECT SUM(net_amount) AS total_net_sales
FROM order_items;

SELECT ROUND(SUM(net_amount) / COUNT(DISTINCT order_id), 2) AS average_order_value
FROM order_items;

SELECT o.store_id, COUNT(DISTINCT o.order_id) AS total_orders
FROM orders o
GROUP BY o.store_id;

SELECT o.store_id, SUM(oi.quantity) AS total_units_sold
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.store_id;

SELECT o.store_id,SUM(oi.net_amount) AS net_sales
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.store_id;

SELECT o.store_id,ROUND(SUM(oi.net_amount) / COUNT(DISTINCT o.order_id),2) AS average_order_value
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.store_id;

SELECT product_id,SUM(quantity) AS total_units_sold
FROM order_items
GROUP BY product_id
ORDER BY total_units_sold DESC;

SELECT product_id,SUM(gross_amount) AS gross_sales
FROM order_items
GROUP BY product_id
ORDER BY gross_sales DESC;

SELECT product_id, SUM(discount) AS total_discount
FROM order_items
GROUP BY product_id
ORDER BY total_discount DESC;

SELECT product_id,SUM(net_amount) AS net_sales
FROM order_items
GROUP BY product_id
ORDER BY net_sales DESC;

SELECT product_id,SUM(net_amount) AS net_sales
FROM order_items
GROUP BY product_id
ORDER BY net_sales DESC
LIMIT 5;

SELECT product_id,SUM(quantity) AS total_units_sold
FROM order_items
GROUP BY product_id
ORDER BY total_units_sold DESC
LIMIT 5;

SELECT strftime('%Y-%m', order_date) AS month,COUNT(*) AS total_orders
FROM orders
GROUP BY month
ORDER BY month;

SELECT strftime('%Y-%m', o.order_date) AS month,SUM(oi.quantity) AS total_units_sold
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY month
ORDER BY month;

SELECT strftime('%Y-%m', o.order_date) AS month,SUM(oi.net_amount) AS net_sales
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY month
ORDER BY month;

WITH monthly_sales AS (SELECT strftime('%Y-%m', o.order_date) AS month,SUM(oi.net_amount) AS net_sales
FROM orders o
JOIN order_items oi
ON o.order_id = oi.order_id
GROUP BY month
)
SELECT month,net_sales,net_sales - LAG(net_sales) OVER (ORDER BY month) AS change_from_previous_month
FROM monthly_sales
ORDER BY month;

-- 5. Monthly Sales Percentage Change
WITH monthly_sales AS (SELECT strftime('%Y-%m', o.order_date) AS month,SUM(oi.net_amount) AS net_sales
FROM orders o
JOIN order_items oi
ON o.order_id = oi.order_id
GROUP BY month
)
SELECT month,net_sales,ROUND((net_sales - LAG(net_sales) OVER (ORDER BY month))* 100.0/ LAG(net_sales) OVER (ORDER BY month),2) AS percentage_change
FROM monthly_sales
ORDER BY month;

SELECT o.store_id,SUM(oi.net_amount) AS net_sales
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.store_id
ORDER BY net_sales DESC
LIMIT 1;

SELECT product_id,SUM(net_amount) AS net_sales
FROM order_items
GROUP BY product_id
ORDER BY net_sales DESC
LIMIT 1;

SELECT product_id,SUM(quantity) AS total_units_sold
FROM order_items
GROUP BY product_id
ORDER BY total_units_sold DESC
LIMIT 1;

SELECT
    strftime('%Y-%m', o.order_date) AS month,
    SUM(oi.net_amount) AS net_sales
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY month
ORDER BY net_sales DESC
LIMIT 1;

SELECT o.store_id,ROUND(SUM(oi.net_amount) / COUNT(DISTINCT o.order_id),2) AS average_order_value
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.store_id
ORDER BY average_order_value DESC
LIMIT 1;
-- F. Monthly Sales Trend using CASE

WITH monthly_sales AS (
    SELECT
        strftime('%Y-%m', o.order_date) AS month,
        SUM(oi.net_amount) AS net_sales
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY month
),
monthly_change AS (
    SELECT
        month,
        net_sales,
        LAG(net_sales) OVER (ORDER BY month) AS previous_sales
    FROM monthly_sales
)
SELECT
    month,
    net_sales,
    CASE
        WHEN previous_sales IS NULL THEN 'N/A'
        WHEN net_sales > previous_sales THEN 'Increase'
        WHEN net_sales < previous_sales THEN 'Decrease'
        ELSE 'No Change'
    END AS sales_trend
FROM monthly_change
ORDER BY month;
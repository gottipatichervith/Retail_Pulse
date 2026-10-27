-- RetailPulse - Use Case 7
-- Data Anomalies & Reconciliation

-- ============================================
-- 1. Duplicate Orders
-- ============================================

SELECT
    order_id,
    COUNT(*) AS occurrence_count
FROM orders
GROUP BY order_id
HAVING COUNT(*) > 1;


-- ============================================
-- 2. Duplicate Order Items
-- ============================================

SELECT
    order_id,
    product_id,
    COUNT(*) AS occurrence_count
FROM order_items
GROUP BY order_id, product_id
HAVING COUNT(*) > 1;


-- ============================================
-- 3. Invalid Customer References
-- ============================================

SELECT
    o.order_id,
    o.customer_id
FROM orders o
LEFT JOIN customers c
    ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;


-- ============================================
-- 4. Invalid Store References
-- ============================================

SELECT
    o.order_id,
    o.store_id
FROM orders o
LEFT JOIN stores s
    ON o.store_id = s.store_id
WHERE s.store_id IS NULL;


-- ============================================
-- 5. Invalid Product References
-- ============================================

SELECT
    oi.order_id,
    oi.product_id
FROM order_items oi
LEFT JOIN products p
    ON oi.product_id = p.product_id
WHERE p.product_id IS NULL;


-- ============================================
-- 6. Invalid Quantities
-- ============================================

SELECT
    order_id,
    product_id,
    quantity
FROM order_items
WHERE quantity <= 0;


-- ============================================
-- 7. Invalid Unit Prices
-- ============================================

SELECT
    order_id,
    product_id,
    unit_price
FROM order_items
WHERE unit_price < 0;


-- ============================================
-- 8. Invalid Discounts
-- ============================================

SELECT
    order_id,
    product_id,
    discount
FROM order_items
WHERE discount < 0;


-- ============================================
-- 9. Discount Greater Than Gross Amount
-- ============================================

SELECT
    order_id,
    product_id,
    gross_amount,
    discount
FROM order_items
WHERE discount > gross_amount;


-- ============================================
-- 10. Invalid Net Amount
-- ============================================

SELECT
    order_id,
    product_id,
    gross_amount,
    discount,
    net_amount
FROM order_items
WHERE net_amount < 0
   OR net_amount != gross_amount - discount;


-- ============================================
-- 11. Product Price Mismatch
-- ============================================

SELECT
    oi.order_id,
    oi.product_id,
    oi.unit_price,
    p.product_price
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
WHERE oi.unit_price != p.product_price;


-- ============================================
-- 12. Unusual High-Value Transactions
-- ============================================

WITH order_values AS (
    SELECT
        order_id,
        SUM(net_amount) AS order_net_sales
    FROM order_items
    GROUP BY order_id
),
sales_statistics AS (
    SELECT
        AVG(order_net_sales) AS average_order_value
    FROM order_values
)
SELECT
    ov.order_id,
    ov.order_net_sales,
    ss.average_order_value
FROM order_values ov
CROSS JOIN sales_statistics ss
WHERE ov.order_net_sales > ss.average_order_value * 2
ORDER BY ov.order_net_sales DESC;
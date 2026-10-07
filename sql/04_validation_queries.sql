SELECT COUNT(*) AS customer_count
FROM customers;

SELECT COUNT(*) AS product_count
FROM products;

SELECT COUNT(*) AS store_count
FROM stores;

SELECT COUNT(*) AS order_count
FROM orders;

SELECT COUNT(*) AS order_item_count
FROM order_items;

SELECT o.order_id, o.customer_id
FROM orders o
LEFT JOIN customers c
    ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;

SELECT oi.order_id, oi.product_id
FROM order_items oi
LEFT JOIN products p
    ON oi.product_id = p.product_id
WHERE p.product_id IS NULL;

SELECT o.order_id, o.store_id
FROM orders o
LEFT JOIN stores s
    ON o.store_id = s.store_id
WHERE s.store_id IS NULL;

SELECT order_id, COUNT(*) AS order_count
FROM orders
GROUP BY order_id
HAVING COUNT(*) > 1;

SELECT order_id, product_id, quantity
FROM order_items
WHERE quantity <= 0;

SELECT order_id, product_id, unit_price
FROM order_items
WHERE unit_price < 0;


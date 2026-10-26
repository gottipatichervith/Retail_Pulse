SELECT
    MAX(order_date) AS analysis_date
FROM orders
WHERE status != 'Cancelled';

SELECT
    o.customer_id,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(oi.quantity) AS units_purchased,
    SUM(oi.net_amount) AS net_spending,
    MIN(o.order_date) AS first_purchase_date,
    MAX(o.order_date) AS most_recent_purchase_date,
    ROUND(
        SUM(oi.net_amount) * 1.0
        / COUNT(DISTINCT o.order_id),
        2
    ) AS average_order_value
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
WHERE o.status != 'Cancelled'
GROUP BY o.customer_id
ORDER BY net_spending DESC;

WITH customer_orders AS (
    SELECT
        customer_id,
        COUNT(DISTINCT order_id) AS total_orders
    FROM orders
    WHERE status != 'Cancelled'
    GROUP BY customer_id
)

SELECT
    CASE
        WHEN total_orders = 1 THEN 'One-time buyer'
        ELSE 'Repeat buyer'
    END AS customer_type,
    COUNT(*) AS customer_count
FROM customer_orders
GROUP BY customer_type;

WITH customer_metrics AS (
    SELECT
        o.customer_id,
        COUNT(DISTINCT o.order_id) AS frequency,
        SUM(oi.net_amount) AS monetary,
        MAX(o.order_date) AS most_recent_purchase_date
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    WHERE o.status != 'Cancelled'
    GROUP BY o.customer_id
)

SELECT
    customer_id,
    CAST(
        julianday('2026-02-10')
        - julianday(most_recent_purchase_date)
        AS INTEGER
    ) AS recency,
    frequency,
    monetary
FROM customer_metrics
ORDER BY monetary DESC;

WITH customer_metrics AS (
    SELECT
        o.customer_id,
        COUNT(DISTINCT o.order_id) AS frequency,
        SUM(oi.net_amount) AS monetary,
        MAX(o.order_date) AS most_recent_purchase_date
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    WHERE o.status != 'Cancelled'
    GROUP BY o.customer_id
),

rfm AS (
    SELECT
        customer_id,
        CAST(
            julianday('2026-02-10')
            - julianday(most_recent_purchase_date)
            AS INTEGER
        ) AS recency,
        frequency,
        monetary
    FROM customer_metrics
)

SELECT
    customer_id,
    recency,
    frequency,
    monetary,
    CASE
        WHEN monetary >= 625 AND recency <= 29
            THEN 'High Value'
        WHEN monetary >= 625 AND recency > 29
            THEN 'At Risk'
        WHEN monetary < 625 AND recency <= 29
            THEN 'Recent Low Engagement'
        ELSE 'Low Engagement'
    END AS customer_segment
FROM rfm
ORDER BY
    customer_segment,
    monetary DESC;

WITH customer_metrics AS (
    SELECT
        o.customer_id,
        COUNT(DISTINCT o.order_id) AS frequency,
        SUM(oi.net_amount) AS monetary,
        MAX(o.order_date) AS most_recent_purchase_date
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    WHERE o.status != 'Cancelled'
    GROUP BY o.customer_id
),

rfm AS (
    SELECT
        customer_id,
        CAST(
            julianday('2026-02-10')
            - julianday(most_recent_purchase_date)
            AS INTEGER
        ) AS recency,
        frequency,
        monetary
    FROM customer_metrics
),

segmented AS (
    SELECT
        customer_id,
        recency,
        frequency,
        monetary,
        CASE
            WHEN monetary >= 625 AND recency <= 29
                THEN 'High Value'
            WHEN monetary >= 625 AND recency > 29
                THEN 'At Risk'
            WHEN monetary < 625 AND recency <= 29
                THEN 'Recent Low Engagement'
            ELSE 'Low Engagement'
        END AS customer_segment
    FROM rfm
)

SELECT
    customer_segment,
    COUNT(*) AS customer_count,
    ROUND(SUM(monetary), 2) AS segment_revenue
FROM segmented
GROUP BY customer_segment
ORDER BY customer_count DESC;


WITH customer_sales AS (
    SELECT
        o.customer_id,
        SUM(oi.net_amount) AS net_spending
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    WHERE o.status != 'Cancelled'
    GROUP BY o.customer_id
),

ranked_customers AS (
    SELECT
        customer_id,
        net_spending,
        ROW_NUMBER() OVER (
            ORDER BY net_spending DESC
        ) AS customer_rank
    FROM customer_sales
)

SELECT
    customer_id,
    net_spending,
    customer_rank
FROM ranked_customers
WHERE customer_rank <= 10
ORDER BY customer_rank;


WITH customer_sales AS (
    SELECT
        o.customer_id,
        SUM(oi.net_amount) AS net_spending
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    WHERE o.status != 'Cancelled'
    GROUP BY o.customer_id
),

top_10 AS (
    SELECT
        customer_id,
        net_spending
    FROM customer_sales
    ORDER BY net_spending DESC
    LIMIT 10
),

total_sales AS (
    SELECT
        SUM(oi.net_amount) AS total_net_sales
    FROM order_items oi
    JOIN orders o
        ON o.order_id = oi.order_id
    WHERE o.status != 'Cancelled'
)

SELECT
    SUM(t.net_spending) AS top_10_sales,
    total_sales.total_net_sales,
    ROUND(
        SUM(t.net_spending) * 100.0
        / total_sales.total_net_sales,
        2
    ) AS top_10_sales_percentage
FROM top_10 t
CROSS JOIN total_sales;

SELECT
    o.customer_id,
    MAX(o.order_date) AS most_recent_purchase_date,
    CAST(
        julianday('2026-02-10')
        - julianday(MAX(o.order_date))
        AS INTEGER
    ) AS days_since_purchase,
    SUM(oi.net_amount) AS net_spending
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
WHERE o.status != 'Cancelled'
GROUP BY o.customer_id
HAVING days_since_purchase > 29
ORDER BY days_since_purchase DESC;

WITH customer_metrics AS (
    SELECT
        o.customer_id,
        SUM(oi.net_amount) AS net_spending,
        MAX(o.order_date) AS most_recent_purchase_date
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    WHERE o.status != 'Cancelled'
    GROUP BY o.customer_id
),

rfm AS (
    SELECT
        customer_id,
        net_spending,
        CAST(
            julianday('2026-02-10')
            - julianday(most_recent_purchase_date)
            AS INTEGER
        ) AS recency
    FROM customer_metrics
)

SELECT
    customer_id,
    recency,
    net_spending
FROM rfm
WHERE
    net_spending >= 625
    AND recency > 29
ORDER BY net_spending DESC;
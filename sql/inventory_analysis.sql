CREATE TABLE IF NOT EXISTS inventory (
    product_id TEXT NOT NULL,
    store_id TEXT NOT NULL,
    current_stock INTEGER NOT NULL CHECK (current_stock >= 0),
    reorder_level INTEGER NOT NULL CHECK (reorder_level >= 0),
    lead_time_days INTEGER NOT NULL CHECK (lead_time_days > 0),

    PRIMARY KEY (product_id, store_id),

    FOREIGN KEY (product_id)
        REFERENCES products(product_id),

    FOREIGN KEY (store_id)
        REFERENCES stores(store_id)
);

WITH sales_summary AS (
    SELECT
        o.store_id,
        oi.product_id,
        SUM(oi.quantity) AS units_sold,
        COUNT(DISTINCT o.order_date) AS selling_days
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY
        o.store_id,
        oi.product_id
)

SELECT store_id,product_id,units_sold,selling_days,
    ROUND(
        units_sold * 1.0 / selling_days,
        2
    ) AS average_daily_demand
FROM sales_summary
ORDER BY store_id,product_id;
WITH sales_summary AS (
    SELECT
        o.store_id,
        oi.product_id,
        SUM(oi.quantity) AS units_sold,
        COUNT(DISTINCT o.order_date) AS selling_days
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY
        o.store_id,
        oi.product_id
),

demand AS (
    SELECT
        store_id,
        product_id,
        units_sold,
        selling_days,
        ROUND(
            units_sold * 1.0 / selling_days,
            2
        ) AS average_daily_demand
    FROM sales_summary
)

SELECT
    d.store_id,
    d.product_id,
    i.current_stock,
    d.units_sold,
    d.average_daily_demand,

    CASE
        WHEN d.average_daily_demand = 0 THEN NULL
        ELSE ROUND(
            i.current_stock * 1.0
            / d.average_daily_demand,
            2
        )
    END AS days_of_stock_remaining

FROM demand d

JOIN inventory i
    ON d.store_id = i.store_id
    AND d.product_id = i.product_id

ORDER BY
    d.store_id,
    d.product_id;
-- Verify inventory data

SELECT *
FROM inventory;

SELECT COUNT(*) AS inventory_rows
FROM inventory;
WITH sales_summary AS (
    SELECT
        o.store_id,
        oi.product_id,
        SUM(oi.quantity) AS units_sold,
        COUNT(DISTINCT o.order_date) AS selling_days
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY
        o.store_id,
        oi.product_id
),

demand AS (
    SELECT
        store_id,
        product_id,
        units_sold,
        selling_days,
        ROUND(
            units_sold * 1.0 / selling_days,
            2
        ) AS average_daily_demand
    FROM sales_summary
)

SELECT
    d.store_id,
    d.product_id,
    i.current_stock,
    d.units_sold,
    d.average_daily_demand,

    CASE
        WHEN d.average_daily_demand = 0 THEN NULL
        ELSE ROUND(
            i.current_stock * 1.0
            / d.average_daily_demand,
            2
        )
    END AS days_of_stock_remaining

FROM demand d

JOIN inventory i
    ON d.store_id = i.store_id
    AND d.product_id = i.product_id

ORDER BY
    d.store_id,
    d.product_id;

-- Task C: Reorder Risk Analysis
WITH sales_summary AS (
    SELECT
        o.store_id,
        oi.product_id,
        SUM(oi.quantity) AS units_sold,
        COUNT(DISTINCT o.order_date) AS selling_days
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY
        o.store_id,
        oi.product_id
),

demand AS (
    SELECT
        store_id,
        product_id,
        units_sold,
        ROUND(
            units_sold * 1.0 / selling_days,
            2
        ) AS average_daily_demand
    FROM sales_summary
),

stock_analysis AS (
    SELECT
        i.store_id,
        i.product_id,
        i.current_stock,
        i.reorder_level,
        i.lead_time_days,
        d.units_sold,
        d.average_daily_demand,

        CASE
            WHEN d.average_daily_demand = 0 THEN NULL
            ELSE ROUND(
                i.current_stock * 1.0
                / d.average_daily_demand,
                2
            )
        END AS days_of_stock_remaining

    FROM inventory i
    LEFT JOIN demand d
        ON i.store_id = d.store_id
        AND i.product_id = d.product_id
)

SELECT
    store_id,
    product_id,
    current_stock,
    reorder_level,
    lead_time_days,
    units_sold,
    average_daily_demand,
    days_of_stock_remaining,

    CASE
        WHEN current_stock = 0
            THEN 'OUT OF STOCK'

        WHEN days_of_stock_remaining < lead_time_days
            THEN 'HIGH RISK'

        WHEN current_stock < reorder_level
            THEN 'REORDER'

        ELSE 'SUFFICIENT'
    END AS inventory_status

FROM stock_analysis

ORDER BY
    store_id,
    product_id;

WITH sales_summary AS (
    SELECT
        o.store_id,
        oi.product_id,
        SUM(oi.quantity) AS units_sold,
        COUNT(DISTINCT o.order_date) AS selling_days
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY
        o.store_id,
        oi.product_id
),

demand AS (
    SELECT
        store_id,
        product_id,
        units_sold,
        ROUND(
            units_sold * 1.0 / selling_days,
            2
        ) AS average_daily_demand
    FROM sales_summary
),

stock_analysis AS (
    SELECT
        i.store_id,
        i.product_id,
        i.current_stock,
        i.reorder_level,
        i.lead_time_days,
        d.units_sold,
        d.average_daily_demand,

        CASE
            WHEN d.average_daily_demand = 0
                THEN NULL
            ELSE ROUND(
                i.current_stock * 1.0
                / d.average_daily_demand,
                2
            )
        END AS days_of_stock_remaining

    FROM inventory i
    LEFT JOIN demand d
        ON i.store_id = d.store_id
        AND i.product_id = d.product_id
)

SELECT
    store_id,
    product_id,
    current_stock,
    reorder_level,
    lead_time_days,
    units_sold,
    average_daily_demand,
    days_of_stock_remaining,

    CASE
        WHEN current_stock = 0
            THEN 'OUT OF STOCK'

        WHEN days_of_stock_remaining < lead_time_days
            THEN 'HIGH RISK'

        WHEN current_stock < reorder_level
            THEN 'REORDER'

        ELSE 'SUFFICIENT'
    END AS inventory_status,

    CASE
        WHEN average_daily_demand IS NULL
            THEN 0

        WHEN
            (average_daily_demand * lead_time_days * 1.20)
            <= current_stock
            THEN 0

        ELSE CAST(
            (
                (average_daily_demand * lead_time_days * 1.20)
                - current_stock
                + 0.9999
            ) AS INTEGER
        )
    END AS suggested_reorder_quantity

FROM stock_analysis

ORDER BY
    store_id,
    product_id;

-- Task D: Business Insights
SELECT
    store_id,
    product_id,
    current_stock
FROM inventory
WHERE current_stock = 0
ORDER BY store_id, product_id;
-- Question 2: Products that may run out before replenishment

WITH demand AS (
    SELECT
        o.store_id,
        oi.product_id,
        SUM(oi.quantity) * 1.0
        / COUNT(DISTINCT o.order_date) AS average_daily_demand
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY
        o.store_id,
        oi.product_id
)

SELECT
    i.store_id,
    i.product_id,
    i.current_stock,
    i.lead_time_days,
    ROUND(
        i.current_stock / d.average_daily_demand,
        2
    ) AS days_of_stock_remaining
FROM inventory i
JOIN demand d
    ON i.store_id = d.store_id
    AND i.product_id = d.product_id
WHERE
    i.current_stock > 0
    AND i.current_stock / d.average_daily_demand < i.lead_time_days
ORDER BY
    i.store_id,
    i.product_id;

WITH demand AS (
    SELECT
        o.store_id,
        oi.product_id,
        SUM(oi.quantity) * 1.0
        / COUNT(DISTINCT o.order_date) AS average_daily_demand
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY
        o.store_id,
        oi.product_id
),

risk_analysis AS (
    SELECT
        i.store_id,
        i.product_id,
        i.current_stock,
        i.lead_time_days,
        CASE
            WHEN i.current_stock = 0
                THEN 'OUT OF STOCK'

            WHEN i.current_stock / d.average_daily_demand
                 < i.lead_time_days
                THEN 'HIGH RISK'

            ELSE 'LOW RISK'
        END AS risk_status
    FROM inventory i
    JOIN demand d
        ON i.store_id = d.store_id
        AND i.product_id = d.product_id
)

SELECT
    store_id,
    COUNT(*) AS total_products,
    SUM(
        CASE
            WHEN risk_status IN ('OUT OF STOCK', 'HIGH RISK')
            THEN 1
            ELSE 0
        END
    ) AS risky_products
FROM risk_analysis
GROUP BY store_id
ORDER BY risky_products DESC;

WITH demand AS (
    SELECT
        o.store_id,
        oi.product_id,
        SUM(oi.quantity) * 1.0
        / COUNT(DISTINCT o.order_date) AS average_daily_demand
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY
        o.store_id,
        oi.product_id
)

SELECT
    i.store_id,
    i.product_id,
    i.current_stock,
    i.reorder_level,
    ROUND(d.average_daily_demand, 2) AS average_daily_demand
FROM inventory i
JOIN demand d
    ON i.store_id = d.store_id
    AND i.product_id = d.product_id
WHERE
    i.current_stock > i.reorder_level
    AND d.average_daily_demand <= 1
ORDER BY
    i.current_stock DESC;

WITH demand AS (
    SELECT
        o.store_id,
        oi.product_id,
        SUM(oi.quantity) * 1.0
        / COUNT(DISTINCT o.order_date) AS average_daily_demand
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY
        o.store_id,
        oi.product_id
),

risk_analysis AS (
    SELECT
        i.store_id,
        i.product_id,
        i.current_stock,
        i.reorder_level,
        i.lead_time_days,
        ROUND(
            i.current_stock / d.average_daily_demand,
            2
        ) AS days_of_stock_remaining,

        CASE
            WHEN i.current_stock = 0
                THEN 'OUT OF STOCK'

            WHEN i.current_stock / d.average_daily_demand
                 < i.lead_time_days
                THEN 'HIGH RISK'

            WHEN i.current_stock < i.reorder_level
                THEN 'REORDER'

            ELSE 'SUFFICIENT'
        END AS inventory_status

    FROM inventory i
    JOIN demand d
        ON i.store_id = d.store_id
        AND i.product_id = d.product_id
)

SELECT
    store_id,
    product_id,
    current_stock,
    days_of_stock_remaining,
    inventory_status,

    CASE
        WHEN inventory_status = 'OUT OF STOCK'
            THEN 1

        WHEN inventory_status = 'HIGH RISK'
            THEN 2

        WHEN inventory_status = 'REORDER'
            THEN 3

        ELSE 4
    END AS priority

FROM risk_analysis
WHERE inventory_status != 'SUFFICIENT'
ORDER BY
    priority,
    store_id,
    product_id;
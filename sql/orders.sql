CREATE TABLE orders (
    order_id TEXT PRIMARY KEY,
    order_date DATE NOT NULL,
    customer_id TEXT NOT NULL,
    store_id TEXT NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (store_id) REFERENCES stores(store_id)
);
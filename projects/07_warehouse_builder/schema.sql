-- 1. Dimensions
CREATE TABLE IF NOT EXISTS dim_product (
    product_key SERIAL PRIMARY KEY,
    original_id INT,
    name VARCHAR(100),
    category VARCHAR(50),
    current_price DECIMAL(10,2)
);

CREATE TABLE IF NOT EXISTS dim_customer (
    customer_key SERIAL PRIMARY KEY,
    original_id INT,
    name VARCHAR(100),
    region VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS dim_date (
    date_key INT PRIMARY KEY, -- YYYYMMDD
    full_date DATE,
    year INT,
    month INT,
    day_name VARCHAR(20)
);

-- 2. Fact Table
CREATE TABLE IF NOT EXISTS fact_sales (
    sales_id SERIAL PRIMARY KEY,
    txn_id INT,
    customer_key INT REFERENCES dim_customer(customer_key),
    product_key INT REFERENCES dim_product(product_key),
    date_key INT REFERENCES dim_date(date_key),
    quantity INT,
    total_amount DECIMAL(10,2)
);

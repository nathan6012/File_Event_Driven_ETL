CREATE TABLE dem_sales_customers(
customer_id SERIAL PRIMARY KEY,
customer_name TEXT NOT NULL,
email TEXT,
created_at TIMESTAMP DEFAULT NOW()
);


CREATE TABLE dem_dates_sales(
date_id DATE PRIMARY KEY,
purchase_date DATE 
);


CREATE TABLE facts_sales(
sales_id SERIAL PRIMARY KEY,
customer_id INT NOT NULL REFERENCES
dem_sales_customers(customer_id),
date_id INT NOT NULL,
purchase_amount NUMERIC NOT NULL,
purchase_quantity NUMERIC NOT NULL,
discount NUMERIC NOT NULL )


USE sales_project;

CREATE TABLE IF NOT EXISTS customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    product_name VARCHAR(100),
    sale_amount DECIMAL(10, 2),
    sale_date DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

INSERT INTO customers (first_name, last_name, email) 
VALUES 
    ('John', 'Doe', 'john.doe@example.com'), 
    ('Jane', 'Smith', 'jane.smith@example.com'), 
    ('Alice', 'Johnson', 'alice.johnson@example.com')
AS new 
ON DUPLICATE KEY UPDATE 
    first_name = new.first_name, 
    last_name = new.last_name, 
    email = new.email;

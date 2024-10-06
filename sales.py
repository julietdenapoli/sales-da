import pandas as pd
from sqlalchemy import create_engine, text  # Import text

# Replace with your RDS details
username = 'admin'  # Your master username
password = 'ears1175'  # Your RDS password
endpoint = 'sales-db.cj2q6iaa60kn.us-east-2.rds.amazonaws.com'  # Your RDS endpoint
database = 'sales_project'  # The name of the database you created


# Create a connection string
connection_string = f'mysql+pymysql://{username}:{password}@{endpoint}/{database}'
engine = create_engine(connection_string)


# Create tables if they do not exist
with engine.connect() as connection:
    connection.execute(text('''
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            email VARCHAR(100)
        );
    '''))
    
    connection.execute(text('''
        CREATE TABLE IF NOT EXISTS sales (
            sale_id INT AUTO_INCREMENT PRIMARY KEY,
            customer_id INT,
            sale_amount DECIMAL(10, 2),
            sale_date DATE,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        );
    '''))

# Insert sample data into the tables
with engine.connect() as connection:
    connection.execute(text('''
        INSERT INTO customers (first_name, last_name, email)
        VALUES 
            ('John', 'Doe', 'john.doe@example.com'), 
            ('Jane', 'Smith', 'jane.smith@example.com')
        ON DUPLICATE KEY UPDATE 
            first_name = VALUES(first_name), 
            last_name = VALUES(last_name), 
            email = VALUES(email);
    '''))

    connection.execute(text('''
        INSERT INTO sales (customer_id, sale_amount, sale_date)
        VALUES 
            (1, 150.00, '2023-10-01'), 
            (1, 200.00, '2023-10-02'), 
            (2, 300.00, '2023-10-01')
        ON DUPLICATE KEY UPDATE 
            sale_amount = VALUES(sale_amount), 
            sale_date = VALUES(sale_date);
    '''))

# Read data into DataFrames
df_customers = pd.read_sql('SELECT * FROM customers', engine)
df_sales = pd.read_sql('SELECT * FROM sales', engine)

# Print the DataFrames to see the fetched data
print("Customers DataFrame:")
print(df_customers)
print("\nSales DataFrame:")
print(df_sales)

# Merge DataFrames to analyze sales by customer
df_merged = pd.merge(df_sales, df_customers, on='customer_id')

# Group by customer and sum the sale amounts
total_sales = df_merged.groupby(['first_name', 'last_name'])['sale_amount'].sum().reset_index()

# Print the total sales by customer
print("\nTotal Sales by Customer:")
print(total_sales)

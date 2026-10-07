# RetailPulse - Retail Data Quality & Ingestion
  

## Project Overview

RetailPulse is a retail data quality and ingestion project.

The purpose of this project is to inspect raw retail sales data, identify data quality issues, clean the valid records, reject invalid records with proper reasons, and prepare reliable data for future analysis.

This project applies Python and pandas concepts learned during internship training.

The project focuses on data quality rather than database operations. A database is not required for this use case.

## Skills Used

- Python
- pandas
- CSV file handling
- Data validation
- Data cleaning
- Basic data analysis
- File handling

## Dataset

The input dataset is:

`retailpulse_usecase1_raw_sales.csv`

The dataset contains the following columns:

| Column | Description |
|---|---|
| `order_id` | Unique sales order identifier |
| `order_date` | Date of the order |
| `store_id` | Store identifier |
| `product_id` | Product identifier |
| `customer_id` | Customer identifier |
| `quantity` | Number of units purchased |
| `unit_price` | Selling price per unit |
| `discount` | Total discount applied to the order line |
| `status` | Order status |

## Business Rules

### Valid Store IDs

The following store IDs are considered valid:

- ST01
- ST02
- ST03

### Valid Product IDs

The following product IDs are considered valid:

- P001
- P002
- P003
- P004
- P005
- P006
- P007

### Valid Order Statuses

The following order statuses are considered valid:
- Completed
- Cancelled
- Pending

## Data Quality Checks

The raw dataset is checked for the following issues.

### 1. Missing Values

Important fields are checked for missing values.
For example, `quantity` must not be missing because it is required to calculate the sales amount.
Missing business values are not invented or guessed.

### 2. Duplicate Records

The dataset is checked for exact duplicate records.
Repeated `order_id` values are not automatically considered duplicates because a single order can contain multiple product lines.

### 3. Invalid Dates

The `order_date` column is checked to make sure that the values can be interpreted as valid dates.
Invalid dates are rejected.

### 4. Invalid Store IDs

The `store_id` value must belong to the list of valid store IDs.

### 5. Invalid Product IDs

The `product_id` value must belong to the list of valid product IDs.

### 6. Invalid Quantity

Quantity must be greater than zero.

Zero or negative quantities are considered invalid.

### 7. Invalid Unit Price

Unit price cannot be negative.

### 8. Invalid Discount

Discount cannot be negative.
The discount also cannot be greater than the gross selling amount.

### 9. Invalid Status

The order status must be one of:
- Completed
- Cancelled
- Pending

## Data Cleaning Rules

The following principles are followed during the cleaning process:
- Missing business values are not invented.
- Invalid records are not silently deleted.
- Rejected records are preserved in a separate output file.
- Rejection reasons are recorded.
- The same validation rules are applied consistently.
- The original raw CSV file is preserved.
- Only records that pass the validation rules are included in the cleaned dataset.

## Validation Process

Each record is checked against the required validation rules.

A record is considered valid when:
- Required values are present.
- Quantity is greater than zero.
- Unit price is not negative.
- Discount is not negative.
- Discount does not exceed the gross amount.
- Store ID is valid.
- Product ID is valid.
- Status is valid.
- Order date is valid.

Records that fail one or more validation checks are treated as rejected records.

## Sales Calculations

For valid records, the following calculations are performed.

### Gross Amount

gross_amount = quantity * unit_price


## Use Case 2 - Database Design & Data Loading

### Objective

The objective of Use Case 2 was to design a relational database for the cleaned RetailPulse sales data and load the data into a SQLite database.

### Database

SQLite was used because it is lightweight, does not require a separate database server, and works easily with Python.

### Database Tables

The database contains five tables:

1. Customers
2. Products
3. Stores
4. Orders
5. Order Items

### Relationships

- One customer can have many orders.
- One store can have many orders.
- One order can contain multiple order items.
- One product can appear in multiple order items.

### Primary and Foreign Keys

Primary keys are used to uniquely identify records.

Foreign keys are used to maintain relationships between tables.

The `order_items` table uses a composite primary key:

```text
(order_id, product_id)
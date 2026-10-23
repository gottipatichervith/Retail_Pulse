# RetailPulse - Sales Performance Report

## 1. Overall Sales Performance

| Metric | Result |
|---|---:|
| Total Orders | 67 |
| Total Units Sold | 92 |
| Total Gross Sales | ₹74,800 |
| Total Discount | ₹1,650 |
| Total Net Sales | ₹73,150 |
| Average Order Value | ₹1,091.79 |

### Summary

The RetailPulse dataset contains 67 orders and 92 units sold.
The total gross sales were ₹74,800, with ₹1,650 provided as discounts. After discounts, the total net sales were ₹73,150.
The average order value was ₹1,091.79, meaning each order generated approximately ₹1,091.79 in net sales on average.

## 2. Store Performance

| Store | Orders | Units Sold | Net Sales | Average Order Value |
|---|---:|---:|---:|---:|
| ST01 | 24 | 33 | ₹24,750 | ₹1,031.25 |
| ST02 | 21 | 29 | ₹25,700 | ₹1,223.81 |
| ST03 | 22 | 30 | ₹22,700 | ₹1,031.82 |

### Best-Performing Store

**ST02** was the best-performing store based on net sales.

- Net Sales: **₹25,700**
- Average Order Value: **₹1,223.81**
- Orders: **21**
- Units Sold: **29**

ST02 generated the highest net sales and also had the highest average order value among the three stores.

## 3. Product Performance

### Product Sales Summary

| Product | Units Sold | Gross Sales | Net Sales |
|---|---:|---:|---:|
| P005 | 13 | ₹19,500 | ₹19,100 |
| P007 | 8 | ₹17,600 | ₹16,900 |
| P002 | 11 | ₹13,200 | ₹12,900 |
| P004 | 12 | ₹9,600 | ₹9,350 |
| P001 | 18 | ₹9,000 | ₹9,000 |
| P003 | 14 | ₹3,500 | ₹3,500 |
| P006 | 16 | ₹2,400 | ₹2,400 |

### Top 5 Products by Net Sales

1. **P005** — ₹19,100
2. **P007** — ₹16,900
3. **P002** — ₹12,900
4. **P004** — ₹9,350
5. **P001** — ₹9,000

### Top 5 Products by Units Sold

1. **P001** — 18 units
2. **P006** — 16 units
3. **P003** — 14 units
4. **P005** — 13 units
5. **P004** — 12 units

### Product Performance Summary

P005 generated the highest net sales at ₹19,100, while P001 sold the highest number of units at 18.
This shows that the product with the highest sales volume was not the product generating the highest revenue. Product price therefore has a significant impact on total revenue.

## 4. Monthly Performance

| Month | Orders | Units Sold | Net Sales |
|---|---:|---:|---:|
| January 2026 | 48 | 73 | ₹56,050 |
| February 2026 | 19 | 19 | ₹17,100 |

### Monthly Sales Trend

January 2026 recorded the highest sales with net sales of ₹56,050.
February 2026 recorded net sales of ₹17,100, representing a decrease of ₹38,950 compared with January.
The percentage decrease in net sales from January to February was **69.49%**.
The SQL analysis classified February's sales trend as **Decrease** using a `CASE` statement and `LAG()` window function.

## 5. Business Questions

### 1. Which store performed the best?
**ST02** was the best-performing store, with net sales of **₹25,700**.

### 2. Which product generated the highest revenue?
**P005** generated the highest net sales, with **₹19,100**.

### 3. Which product sold the most units?
**P001** sold the highest number of units, with **18 units**.

### 4. Which month had the highest sales?
**January 2026** had the highest net sales, with **₹56,050**.

### 5. Which store had the highest average order value?
**ST02** had the highest average order value at **₹1,223.81**.

### 6. Does the best-selling product also generate the highest revenue?
**No.** P001 sold the most units (18), while P005 generated the highest net sales (₹19,100).

This shows that sales volume and revenue are not always the same because product prices can differ.

## 6. Key Business Insights
1. **ST02 was the strongest-performing store.**  
   It generated the highest net sales of ₹25,700 and the highest average order value of ₹1,223.81.
2. **P005 was the highest-revenue product.**  
   It generated ₹19,100 in net sales, even though it sold fewer units than P001.
3. **P001 had the highest sales volume.**  
   It sold 18 units, making it the top product by quantity sold.
4. **January 2026 was significantly stronger than February 2026.**  
   Net sales decreased from ₹56,050 in January to ₹17,100 in February, a 69.49% decrease.
5. **Sales volume and revenue were not directly correlated.**  
   P001 sold the most units, while P005 generated the highest revenue. This indicates that product price influences revenue in addition to sales volume.

## 7. Validation
The SQL analysis results were validated against the cleaned sales data and the SQLite database created in Use Case 2.

### Validation Results

| Validation Check | Result |
|---|---:|
| Total Orders | 67 |
| Total Units Sold | 92 |
| Total Gross Sales | ₹74,800 |
| Total Discount | ₹1,650 |
| Total Net Sales | ₹73,150 |
| Average Order Value | ₹1,091.79 |

The total net sales of **₹73,150** match the validated database totals from Use Case 2.
The database validation also confirmed:
- No invalid customer references
- No invalid product references
- No invalid store references
- No duplicate order IDs
- No invalid quantities
- No negative prices

### Overall Result
The sales analysis was successfully completed using SQL on the RetailPulse SQLite database. The results provide insights into overall sales, store performance, product performance, and monthly sales trends.
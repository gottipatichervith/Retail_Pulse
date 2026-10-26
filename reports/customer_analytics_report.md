# RetailPulse - Customer Analytics & Segmentation Report

## 1. Objective

The objective of this analysis is to understand customer purchasing behavior, identify customer segments, and find customers who may need retention attention.

## 2. Analysis Date

The analysis date is **2026-02-10**.

## 3. RFM Methodology

- **Recency:** Number of days since the customer's most recent purchase.
- **Frequency:** Number of distinct orders placed by the customer.
- **Monetary:** Total net spending by the customer.

## 4. Segmentation Rules

| Segment | Rule |
|---|---|
| High Value | Spending >= ₹625 and Recency <= 29 days |
| At Risk | Spending >= ₹625 and Recency > 29 days |
| Recent Low Engagement | Spending < ₹625 and Recency <= 29 days |
| Low Engagement | Spending < ₹625 and Recency > 29 days |

## 5. Segment Summary

| Segment | Customers | Revenue |
|---|---:|---:|
| At Risk | 13 | ₹17,400.00 |
| High Value | 31 | ₹48,100.00 |
| Low Engagement | 5 | ₹2,150.00 |
| Recent Low Engagement | 18 | ₹5,500.00 |

## 6. Repeat vs One-time Customers

- **One-time buyer:** 67 customers

## 7. Revenue by Customer Type

- **One-time buyer:** ₹73,150.00

## 8. Top 10 Customers

| Rank | Customer | Net Spending | Segment |
|---:|---|---:|---|
| 1 | C024 | ₹3,000.00 | High Value |
| 2 | C036 | ₹2,900.00 | High Value |
| 3 | C019 | ₹2,900.00 | High Value |
| 4 | C016 | ₹2,300.00 | At Risk |
| 5 | C069 | ₹2,200.00 | High Value |
| 6 | C062 | ₹2,200.00 | High Value |
| 7 | C055 | ₹2,200.00 | High Value |
| 8 | C015 | ₹2,200.00 | At Risk |
| 9 | C027 | ₹2,100.00 | High Value |
| 10 | C041 | ₹2,000.00 | High Value |

## 9. Top 10 Revenue Contribution

The top 10 customers generated **₹24,000.00**, representing **32.81%** of total eligible net sales of **₹73,150.00**.

## 10. Customers Who Have Not Purchased Recently

There are **18 customers** with more than 29 days since their most recent purchase.

| Customer | Recency | Net Spending | Segment |
|---|---:|---:|---|
| C001 | 38 days | ₹1,000.00 | At Risk |
| C002 | 38 days | ₹1,100.00 | At Risk |
| C004 | 37 days | ₹750.00 | At Risk |
| C003 | 37 days | ₹750.00 | At Risk |
| C006 | 36 days | ₹1,300.00 | At Risk |
| C005 | 36 days | ₹1,000.00 | At Risk |
| C008 | 35 days | ₹1,200.00 | At Risk |
| C007 | 35 days | ₹600.00 | Low Engagement |
| C010 | 34 days | ₹2,000.00 | At Risk |
| C009 | 34 days | ₹500.00 | Low Engagement |
| C012 | 33 days | ₹1,500.00 | At Risk |
| C011 | 33 days | ₹1,500.00 | At Risk |
| C013 | 32 days | ₹500.00 | Low Engagement |
| C014 | 32 days | ₹300.00 | Low Engagement |
| C016 | 31 days | ₹2,300.00 | At Risk |
| C015 | 31 days | ₹2,200.00 | At Risk |
| C018 | 30 days | ₹800.00 | At Risk |
| C017 | 30 days | ₹250.00 | Low Engagement |

## 11. Business Recommendations

- Prioritize **At Risk** customers for retention campaigns.
- Focus especially on high-spending At Risk customers.
- Encourage one-time buyers to make a second purchase.
- Use targeted offers for Recent Low Engagement customers.
- Monitor customer activity as more historical data becomes available.

## 12. Limitations

- The dataset covers a limited historical period.
- All customers currently have only one eligible order, so repeat purchase behavior cannot be measured yet.
- At Risk is a recency-based signal and should not be interpreted as confirmed customer churn.
- Segmentation thresholds were derived from the current dataset and may change as more data becomes available.

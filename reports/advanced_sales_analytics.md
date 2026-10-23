# RetailPulse – Advanced Sales Analytics Report

## 1. Product Ranking

### Overall Product Ranking

Products were ranked based on total net sales.

| Rank | Product | Net Sales |
|---|---|---:|
| 1 | P005 | ₹19,100 |
| 2 | P007 | ₹16,900 |
| 3 | P002 | ₹12,900 |
| 4 | P004 | ₹9,350 |
| 5 | P001 | ₹9,000 |
| 6 | P003 | ₹3,500 |
| 7 | P006 | ₹2,400 |

**Finding:** P005 generated the highest net sales.

### Top 3 Products by Store

| Store | Top Products |
|---|---|
| ST01 | P007, P002, P005 |
| ST02 | P005, P007, P002, P004 |
| ST03 | P002, P005, P007 |

ST02 has four products in the top 3 because P002 and P004 have the same sales rank.

### Ranking Functions

- `ROW_NUMBER()` gives every product a unique position.
- `RANK()` gives the same rank to products with equal sales and skips the next rank.
- `DENSE_RANK()` gives the same rank to ties without skipping a rank.

---

## 2. Running Sales Totals

Cumulative net sales were calculated by date and separately for each store.

The final cumulative sales were:

| Store | Cumulative Net Sales |
|---|---:|
| ST01 | ₹24,750 |
| ST02 | ₹25,700 |
| ST03 | ₹22,700 |

The overall cumulative net sales reached **₹73,150**.

**Finding:** Running totals show how sales build over time, while a normal `SUM()` gives only the total for a group.

---

## 3. Month-over-Month Sales

| Month | Net Sales | Previous Month | Change | Change % |
|---|---:|---:|---:|---:|
| Jan 2026 | ₹56,050 | — | — | — |
| Feb 2026 | ₹17,100 | ₹56,050 | -₹38,950 | -69.49% |

**Finding:** Net sales decreased by **69.49%** in February compared with January.

The first month has no previous month, so its comparison is `NULL`.

---

## 4. Product Sales Contribution

| Product | Net Sales | Contribution |
|---|---:|---:|
| P005 | ₹19,100 | 26.11% |
| P007 | ₹16,900 | 23.10% |
| P002 | ₹12,900 | 17.63% |
| P004 | ₹9,350 | 12.78% |
| P001 | ₹9,000 | 12.30% |
| P003 | ₹3,500 | 4.78% |
| P006 | ₹2,400 | 3.28% |

The top four products — **P005, P007, P002, and P004** — generated approximately **79.62%** of total net sales.

**Finding:** Sales are concentrated among a small number of products.

---

## 5. Key Business Insights

1. **P005** is the highest-revenue product with ₹19,100 net sales.
2. **ST02** has the highest store-level net sales at ₹25,700.
3. February sales decreased significantly compared with January.
4. The top four products contribute approximately **80% of total net sales**.
5. The best-selling product by revenue is different from the product with the highest units sold, showing that sales volume and revenue are not always the same.

---

## 6. Conclusion

Advanced SQL analysis using window functions, CTEs, ranking, and date comparisons provided deeper insights into product, store, and monthly sales performance.

The analysis shows that RetailPulse sales are concentrated among a few high-performing products and that February experienced a significant decline in sales.
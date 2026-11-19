
# SQL Analysis Report

## 1. Introduction

SQL analysis was performed to extract meaningful business insights from the Supply Chain dataset. The analysis focuses on shipment performance, delivery delays, shipping modes, customer segments, and regional distribution.

## 2. Database Overview

- Database: `supply_chain.db`
- Database Type: SQLite
- Source: DataCo Smart Supply Chain Dataset
- Purpose: Structured storage and analysis of supply chain records.

The database schema and SQL queries are maintained in the `sql/` directory.

## 3. SQL Analysis Performed

The following analysis areas were explored:

1. Total shipment and order analysis.
2. Delivery status distribution.
3. Late delivery percentage.
4. Shipping mode performance.
5. Customer segment analysis.
6. Regional shipment performance.
7. Monthly delivery trends.
8. Product and category-level analysis.

## 4. Key Business Findings

### Delivery Performance

- Original dataset contains 180,519 records.
- Late delivery accounts for 98,977 records.
- After excluding canceled shipments, the late-delivery rate is 57.29%.

### Shipping Mode Performance

| Shipping Mode  | Total Shipments | Late Shipments | Late Rate |
| -------------- | --------------: | -------------: | --------: |
| First Class    |          26,513 |         26,513 |   100.00% |
| Second Class   |          33,806 |         26,987 |    79.83% |
| Same Day       |           9,293 |          4,454 |    47.93% |
| Standard Class |         103,153 |         41,023 |    39.77% |

### Regional Performance

- Central Africa recorded a 60.15% late-delivery rate.
- Central America had the highest shipment volume, with 27,174 shipments.

### Customer Segment Performance

Late-delivery percentages were similar across Home Office, Consumer, and Corporate segments.

## 5. Business Insights

1. First Class shipments require further investigation because of their high observed late-delivery rate.
2. Shipping mode is an important dimension for delivery performance monitoring.
3. Regional shipment analysis can help identify areas requiring operational attention.
4. Delivery trends can help supply chain teams understand historical performance.
5. SQL makes it possible to extract these insights efficiently from structured shipment data.

## 6. SQL Techniques Used

The project uses SQL concepts such as:

- SELECT and WHERE
- GROUP BY
- ORDER BY
- Aggregate functions such as COUNT, SUM, and AVG
- CASE WHEN conditions
- Subqueries
- Date-based grouping
- Percentage calculations

## 7. Business Recommendations

- Monitor late-delivery percentages by shipping mode.
- Investigate regions with higher delay rates.
- Track monthly delivery performance.
- Use SQL-generated insights alongside the machine learning dashboard.
- Regularly validate the quality and consistency of shipment records.

## 8. Conclusion

SQL analysis provided a structured way to explore supply chain operations and identify delivery performance patterns. These insights support the project's EDA, predictive modeling, and dashboard development.

## 9. Limitations

- The analysis is based on historical data from 2015–2018.
- Observed relationships do not establish causation.
- Historical findings should not be treated as current operational performance.


# Exploratory Data Analysis (EDA) Summary

## 1. Introduction

Exploratory Data Analysis (EDA) was performed to understand the Supply Chain dataset, identify delivery patterns, analyze shipment performance, and discover factors associated with late deliveries.

## 2. Dataset Overview

| Property                 | Details                           |
| ------------------------ | --------------------------------- |
| Dataset                  | DataCo Smart Supply Chain Dataset |
| Original Records         | 180,519                           |
| Cleaned Dataset Records  | 180,519                           |
| Cleaned Dataset Features | 51                                |
| Historical Period        | 2015–2018                        |
| Data Type                | Structured tabular data           |

## 3. Delivery Status Distribution

The dataset contains four delivery status categories.

| Delivery Status   | Records |
| ----------------- | ------: |
| Late delivery     |  98,977 |
| Advance shipping  |  41,592 |
| Shipping on time  |  32,196 |
| Shipping canceled |   7,754 |

Late delivery represents the largest category in the dataset.

## 4. Delivery Performance Analysis

For delivery performance calculations and model training, canceled shipments were excluded.

| Metric                |   Value |
| --------------------- | ------: |
| Valid Shipments       | 172,765 |
| Late Shipments        |  98,977 |
| Late Delivery Rate    |  57.29% |
| On-Time Shipments     |  32,196 |
| On-Time Rate          |  18.64% |
| Advance Shipments     |  41,592 |
| Advance Shipping Rate |  24.07% |

## 5. Shipping Mode Analysis

| Shipping Mode  | Total Shipments | Late Shipments | Late Rate |
| -------------- | --------------: | -------------: | --------: |
| First Class    |          26,513 |         26,513 |   100.00% |
| Second Class   |          33,806 |         26,987 |    79.83% |
| Same Day       |           9,293 |          4,454 |    47.93% |
| Standard Class |         103,153 |         41,023 |    39.77% |

First Class has the highest observed late-delivery rate, while Standard Class has the lowest among the four shipping modes.

## 6. Customer Segment Analysis

| Customer Segment | Late Delivery Rate |
| ---------------- | -----------------: |
| Home Office      |             57.59% |
| Consumer         |             57.31% |
| Corporate        |             57.08% |

Late-delivery rates are relatively similar across customer segments.

## 7. Regional Analysis

- Central Africa recorded the highest observed late-delivery rate at 60.15%.
- Central America recorded the highest shipment volume, with 27,174 shipments.
- Regional analysis helps identify areas that may require further investigation.

## 8. Monthly Delivery Trends

- The dataset covers 37 months, from January 2015 to January 2018.
- Monthly late-delivery rates ranged from approximately 55.17% to 59.31%.
- June 2016 recorded the highest monthly late-delivery rate.
- July 2016 recorded the lowest monthly late-delivery rate.

## 9. Key EDA Findings

1. Late deliveries form the largest delivery-status category.
2. More than half of valid shipments were delivered late.
3. First Class shipping recorded a 100% late-delivery rate in this dataset.
4. Customer segment differences were relatively small.
5. Regional and monthly patterns provide useful areas for further investigation.
6. Shipping mode and scheduled shipment duration were also important features in the trained prediction model.

## 10. Business Recommendations

- Investigate the operational reasons behind high late-delivery rates for First Class shipments.
- Monitor regions with comparatively high late-delivery percentages.
- Review scheduled delivery durations and shipment planning.
- Track delivery performance regularly using dashboards.
- Use predictive risk scores as decision-support signals, not as guaranteed outcomes.

## 11. Limitations

- The dataset contains historical records from 2015–2018.
- Observed patterns do not necessarily represent current supply chain conditions.
- Statistical associations do not establish causation.
- Findings depend on the available dataset and its quality.

## 12. Conclusion

EDA revealed important patterns in shipment performance, shipping modes, customer segments, and geographical regions. These findings helped guide feature selection, model development, and the design of the interactive supply chain dashboard.

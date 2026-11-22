# Business Analyst Technical Assessment

**A comprehensive hotel booking data analysis project covering data quality, customer segmentation, revenue analysis, SQL querying, and multi-currency reporting.**

**Repository:** [Business-Analyst-Assessment](https://github.com/alo7lika/Business-Analyst-Assessment)

## Project Overview

This project analyzes hotel booking data to identify data quality issues, understand customer booking behavior, evaluate high-value customer segments, investigate revenue patterns, and generate actionable business insights.

The assessment is divided into four sections, combining Python-based data analysis, PostgreSQL, SQL, data visualization, and historical foreign exchange rate analysis.

## Project Objectives

- Identify inconsistencies, missing values, and data quality issues in hotel booking records.
- Analyze customer behavior and identify high-value customers using multiple VIP definitions.
- Compare customer acquisition and retention strategies.
- Design a relational database schema and write SQL queries for business analysis.
- Analyze monthly revenue in INR and USD using historical exchange rates.
- Present findings through structured reports, tables, and visualizations.

## Project Structure

```text
Business-Analyst-Assessment/
│
├── Section 1 & 2/
│   ├── Data Quality Analysis
│   ├── Customer Segmentation
│   └── Business Analysis and Visualizations
│
├── Section 3/
│   ├── schema.sql
│   ├── import_table.sql
│   └── queries.sql
│
├── Section 4/
│   ├── multi_currency_report.py
│   ├── multi_currency_revenue_report.csv
│   ├── monthly_revenue_inr.png
│   ├── monthly_revenue_usd.png
│   └── README.txt
│
├── hotel_bookings.xlsx
├── hotel_bookings.csv
└── README.md
```

## Section 1 – Data Quality and Forensics

Performed data quality checks on the hotel booking dataset to identify inconsistencies and potential reporting risks.

Key checks included:

- Bookings with zero rooms.
- Bookings created before customer registration.
- Missing customer reviews.
- Booking amount formula mismatches.
- Invalid check-in and check-out dates.
- Review availability across booking statuses.

### Key Findings

| Data quality check | Result |
|---|---:|
| Zero-room bookings | 60 |
| Bookings before customer signup | 364 |
| Bookings without reviews | 6,924 |
| Missing review percentage | 57.70% |
| Invalid stays | 120 |
| Total amount formula mismatches | 35 |
| Mismatches among completed bookings | 26 |

These findings highlight potential data integrity and reporting issues that should be considered before using the dataset for business decisions.

## Section 2 – Customer Segmentation and Business Analysis

Analyzed customer value using three VIP definitions:

1. **Spend-based VIP:** Customers in the top 10% by realized spending.
2. **Booking-frequency VIP:** Customers in the top 10% by completed booking count.
3. **Lifetime-value-rate VIP:** Customers in the top 10% by the defined lifetime-value rate.

The analysis examined the overlap between these customer groups and compared VIP and non-VIP booking behavior.

### Customer Segmentation Results

| Metric | Result |
|---|---:|
| Total customers | 5,464 |
| Top 10% per VIP definition | 547 |
| Customers in all three VIP groups | 255 |
| Customers in exactly two groups | 271 |
| Customers in only one group | 334 |
| Customers in none of the groups | 4,604 |

### Revenue and Retention Insights

- Spend-based VIP customers contributed approximately **47.64% of realized revenue**.
- VIP cancellation rate: **15.48%**.
- Non-VIP cancellation rate: **21.31%**.
- VIP customers demonstrated a lower observed cancellation rate.
- Discount intensity was broadly similar between VIP and non-VIP customers.

The analysis also evaluated acquisition versus retention investment to support customer growth and retention decisions.

## Section 3 – Database Design and SQL Analysis

Designed a normalized relational database schema using PostgreSQL.

### Database Tables

- `customers`
- `properties`
- `bookings`
- `reviews`

The schema includes primary keys, foreign keys, constraints, and an index to support customer booking sequence queries.

A flat import table, `hotel_bookings`, was also created to load the source dataset and execute the assessment queries.

### SQL Analysis

**Query 1 – Average Booking Amount by Booking Sequence**

Used window functions and `ROW_NUMBER()` to classify completed bookings into:

- First booking
- Second booking
- Third or later booking

| Booking sequence | Average booking amount | Count |
|---|---:|---:|
| First | ₹29,765.24 | 4,719 |
| Second | ₹29,328.32 | 1,884 |
| Third or Later | ₹30,197.68 | 2,676 |

**Query 2 – Top Five Properties by Normalized Average Review Rating**

- Converted Corporate customer ratings from a 1–10 scale to a 1–5 scale.
- Excluded reviews associated with cancelled bookings.
- Included properties with at least 20 reviews.
- Ranked properties by normalized average rating.

The queries are available in `Section 3/queries.sql`, and the database design is available in `Section 3/schema.sql`.

## Section 4 – Multi-Currency Revenue Analysis

Developed a Python-based reporting script to analyze monthly realized revenue in Indian Rupees (INR) and US Dollars (USD).

### Methodology

- Used completed bookings for realized revenue calculations.
- Retrieved historical USD/INR exchange rates through the Frankfurter API.
- Applied the first available exchange rate in each month.
- Generated monthly revenue reports in INR and USD.
- Created separate visualizations for both currencies.
- Compared revenue growth over the common full-month period.

### Key Findings

For the comparable period from October 2023 to November 2024:

| Metric | Result |
|---|---:|
| INR revenue growth | 1,067.62% |
| USD revenue growth | 1,055.29% |
| Difference after FX adjustment | 12.33 percentage points |

The USD-denominated analysis shows slightly lower revenue growth than the INR figures, demonstrating the impact of exchange-rate movements on international revenue comparisons.

### Generated Outputs

- `multi_currency_revenue_report.csv`
- `monthly_revenue_inr.png`
- `monthly_revenue_usd.png`

## Technologies and Tools

| Technology | Application |
|---|---|
| Python | Data processing and analysis |
| Pandas | Data manipulation and aggregation |
| PostgreSQL | Relational database management |
| SQL | Data querying and business analysis |
| Matplotlib | Data visualization |
| Excel | Dataset inspection and preparation |
| Frankfurter API | Historical foreign exchange rates |
| Git and GitHub | Version control and project hosting |

## How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/alo7lika/Business-Analyst-Assessment.git
cd Business-Analyst-Assessment
```

### 2. Install Python Dependencies

```bash
pip install pandas openpyxl matplotlib requests
```

### 3. Run the Multi-Currency Analysis

Ensure the source Excel dataset is available in the project root, then execute:

```bash
python "Section 4/multi_currency_report.py"
```

The script generates the monthly revenue CSV report and INR/USD visualizations in the Section 4 directory.

### 4. Execute SQL Analysis

Install PostgreSQL and create the assessment database.

Execute the SQL scripts in the following order:

1. `Section 3/schema.sql`
2. `Section 3/import_table.sql`
3. Import the CSV dataset into the flat table.
4. `Section 3/queries.sql`

## Business Value

This project demonstrates how data analytics can support business decision-making through:

- Improved data quality and reporting reliability.
- Customer segmentation and identification of high-value customers.
- Evidence-based acquisition and retention analysis.
- Database design and SQL-based business intelligence.
- Revenue trend analysis and foreign exchange impact assessment.

## Author

**Alolika Bhowmik**

[GitHub](https://github.com/alo7lika) | [LinkedIn](https://www.linkedin.com/in/alolika-bhowmik72/) | [Portfolio](https://alo7lika.github.io/Portfolio-/)

---

*This repository contains the work completed for the Business Analyst Technical Assessment.*

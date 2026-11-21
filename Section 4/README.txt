# Multi-Currency Revenue Reporter — Question Set C

## 1. Purpose
Converts realized hotel booking revenue from INR into USD, EUR, and GBP using historical monthly exchange rates.

## 2. Input
- `hotel_bookings.xlsx` must be placed in the main Assignment folder.
- The script reads only bookings with status `Completed`.

## 3. Requirements
Install the required libraries:

```bash
pip install pandas requests matplotlib openpyxl
```

## 4. Execution
Run from the main Assignment folder:

```bash
python "Section 4/multi_currency_report.py"
```

## 5. Exchange Rate Methodology
- Uses historical exchange rates from the Frankfurter API.
- INR is the base currency.
- Retrieves USD, EUR, and GBP rates for each booking month.
- Selects the first available business-day rate within that month.
- Stops execution if exchange-rate data is unavailable rather than inventing or filling missing rates.

## 6. Outputs
All generated files are saved in the Section 4 folder:

- `multi_currency_revenue_report.csv`
- `monthly_revenue_inr.png`
- `monthly_revenue_usd.png`

## 7. Revenue Comparison
The comparable-period analysis excludes incomplete first and last months. For this dataset, October 2023 to November 2024 is used.

- INR revenue growth: 1,067.62%
- USD revenue growth: 1,055.29%
- FX adjustment: 12.33 percentage points

## 8. Limitation
Monthly conversion uses the first available business-day exchange rate rather than daily booking-date rates or a monthly average rate.

"""
Multi-Currency Revenue Reporter — Question Set C
Run from a directory containing hotel_bookings.xlsx:
    pip install pandas requests matplotlib openpyxl
    python multi_currency_report.py

Uses monthly historical FX rates from Frankfurter. The rate is the first
available quoted business-day rate in each month, not a fabricated month-end
or daily-weighted rate. Only Completed bookings count as realized revenue.
"""
import pandas as pd
import requests
import matplotlib.pyplot as plt

INPUT = "hotel_bookings.xlsx"
OUTPUT = "Section 4/multi_currency_revenue_report.csv"
CURRENCIES = "USD,EUR,GBP"


def get_monthly_rate(month, session=requests):
    start = pd.Period(month, freq="M").start_time.date().isoformat()
    end = pd.Period(month, freq="M").end_time.date().isoformat()

    url = f"https://api.frankfurter.app/{start}..{end}?base=INR&symbols={CURRENCIES}"

    response = session.get(url, timeout=20)
    response.raise_for_status()

    payload = response.json()
    rates = payload.get("rates", {})

    # Select only dates belonging to the requested month.
    valid_dates = sorted(
        date for date in rates
        if date.startswith(month + "-")
    )

    if not valid_dates:
        raise ValueError(f"No exchange rates available within {month}")

    first_date = valid_dates[0]
    return first_date, rates[first_date]

def main():
    df = pd.read_excel(INPUT, keep_default_na=False)
    df["booking_date"] = pd.to_datetime(df["booking_date"], errors="coerce")
    df["total_amount"] = pd.to_numeric(df["total_amount"], errors="coerce")
    realized = df[df["booking_status"].eq("Completed")].copy()
    realized = realized.dropna(subset=["booking_date", "total_amount"])
    realized["month"] = realized["booking_date"].dt.to_period("M").astype(str)

    monthly = (realized.groupby("month")
               .agg(bookings=("booking_id", "count"),
                    revenue_inr=("total_amount", "sum"))
               .reset_index())

    rate_rows = []
    for month in monthly["month"]:
        try:
            rate_date, rates = get_monthly_rate(month)
            rate_rows.append({"month": month, "rate_date": rate_date, **rates})
        except (requests.RequestException, ValueError, KeyError, TypeError) as exc:
            print(f"ERROR: FX lookup failed for {month}: {exc}")
            print("Stopping rather than filling missing rates with invented values.")
            raise SystemExit(1)

    fx = pd.DataFrame(rate_rows)
    report = monthly.merge(fx, on="month", how="left", validate="one_to_one")
    for currency in ["USD", "EUR", "GBP"]:
        if report[currency].isna().any():
            raise ValueError(f"Missing {currency} rate; report not exported.")
        report[f"revenue_{currency.lower()}"] = report["revenue_inr"] * report[currency]

    report.to_csv(OUTPUT, index=False)
    print(report.to_string(index=False))

    # Exclude the last partial month if the source dataset ends mid-month.
    last_booking_date = realized["booking_date"].max()
    first_booking_date = realized["booking_date"].min()
    first_month = str(first_booking_date.to_period("M"))
    last_month = str(last_booking_date.to_period("M"))
    
    full_months = report[
        (report["month"] > first_month) &
        (report["month"] < last_month)
        ].copy()
    
    if len(full_months) >= 2:
        start, end = full_months.iloc[0], full_months.iloc[-1]
        inr_change = (end.revenue_inr / start.revenue_inr - 1) * 100
        usd_change = (end.revenue_usd / start.revenue_usd - 1) * 100
        print(f"Comparable period: {start.month} to {end.month}")
        print(f"INR revenue change: {inr_change:.2f}%")
        print(f"USD revenue change: {usd_change:.2f}%")
        print(f"FX adjustment (percentage-point difference): {inr_change-usd_change:.2f} pp")

        ax = full_months.plot(x="month", y="revenue_inr", marker="o",
                              title="Monthly realized revenue in INR")
        ax.set_ylabel("INR")
        plt.tight_layout()
        plt.savefig("Section 4/monthly_revenue_usd.png", dpi=160)
        plt.close()

        ax = full_months.plot(x="month", y="revenue_usd", marker="o",
                              title="Monthly realized revenue in USD")
        ax.set_ylabel("USD")
        plt.tight_layout()
        plt.savefig("Section 4/monthly_revenue_inr.png", dpi=160)
        plt.close()

if __name__ == "__main__":
    main()

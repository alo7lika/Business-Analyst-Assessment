import pandas as pd
import numpy as np
import math
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

INPUT = "hotel_bookings.xlsx"
df = pd.read_excel(INPUT, keep_default_na=False)
for c in ["booking_date","checkin_date","checkout_date","customer_signup_date","review_date"]:
    df[c] = pd.to_datetime(df[c], errors="coerce")
for c in ["num_rooms","nights","adr","discount_amount","total_amount","review_rating"]:
    df[c] = pd.to_numeric(df[c], errors="coerce")

# Section 1
print("DQ1 zero rooms:", int((df.num_rooms == 0).sum()))
print("DQ2 booking before signup:", int((df.booking_date < df.customer_signup_date).sum()))
print("DQ3 no review:", int(df.review_rating.isna().sum()),
      f"({df.review_rating.isna().mean()*100:.2f}%)")
print(df.assign(no_review=df.review_rating.isna()).groupby("booking_status").no_review.agg(["sum","count"]))
print("Invalid stays:", int((df.checkout_date <= df.checkin_date).sum()))
expected = df.adr * df.nights * df.num_rooms - df.discount_amount
mismatch = (expected - df.total_amount).abs() > 0.02
print("Undocumented amount formula mismatches:", int(mismatch.sum()),
      "Completed:", int((mismatch & df.booking_status.eq("Completed")).sum()))

# Section 2: use all distinct customers, including zero-completed-booking customers
completed = df[df.booking_status.eq("Completed")].copy()
snapshot = df.booking_date.max()
base = df.groupby("customer_id").agg(signup=("customer_signup_date","min")).reset_index()
agg = completed.groupby("customer_id").agg(spend=("total_amount","sum"),
                                             booking_count=("booking_id","count")).reset_index()
cust = base.merge(agg, on="customer_id", how="left")
cust[["spend","booking_count"]] = cust[["spend","booking_count"]].fillna(0)
cust["months"] = ((snapshot - cust.signup).dt.days / 30.4375).clip(lower=1)
cust["ltv_rate"] = cust.spend / cust.months
k = math.ceil(0.10 * len(cust))
sets = {}
for metric in ["spend","booking_count","ltv_rate"]:
    sets[metric] = set(cust.sort_values([metric,"customer_id"], ascending=[False,True]).head(k).customer_id)
regions = Counter()
for cid in cust.customer_id:
    regions[sum(cid in s for s in sets.values())] += 1
print("Customers:", len(cust), "Top 10% per definition:", k)
print("In all three:", regions[3], "Exactly two:", regions[2], "Only one:", regions[1])
vip_ids = sets["spend"]
df["is_vip"] = df.customer_id.isin(vip_ids)
realized = completed.total_amount.sum()
vip_revenue = completed[completed.customer_id.isin(vip_ids)].total_amount.sum()
print("Realized revenue:", realized, "VIP realized revenue share:", vip_revenue/realized*100)
for flag, sub in df.groupby("is_vip"):
    print("VIP" if flag else "Non-VIP",
          "cancellation rate", (sub.booking_status.eq("Cancelled").mean()*100),
          "discount intensity", sub.discount_amount.sum() /
          (sub.adr*sub.nights*sub.num_rooms).sum()*100)

# Section 3 query result cross-check
ranked = completed.sort_values(["customer_id","checkin_date","booking_id"]).copy()
ranked["rn"] = ranked.groupby("customer_id").cumcount()+1
ranked["sequence"] = np.select([ranked.rn.eq(1),ranked.rn.eq(2)],
                                ["First","Second"], default="Third or Later")
print(ranked.groupby("sequence").total_amount.agg(["mean","count"]).reindex(
    ["First","Second","Third or Later"]))

# Section 4 is in ../project/multi_currency_report.py

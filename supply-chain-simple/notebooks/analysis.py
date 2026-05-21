"""
analysis.py
Supply Chain Analysis — EDA + Reorder Point Model
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ── Load data ─────────────────────────────────────────────────────────────────
df = pd.read_csv("data/sample_data.csv", parse_dates=["order_date"])
print(f"Dataset: {len(df):,} rows\n")

# ── 1. Late delivery rate by supplier ─────────────────────────────────────────
df["is_late"] = df["actual_lead_time_days"] > df["promised_lead_time_days"]

supplier_perf = (df.groupby("supplier_id")
                   .agg(total_orders=("order_id","count"),
                        late_pct=("is_late", lambda x: round(x.mean()*100,1)),
                        avg_defect=("defect_rate_pct","mean"))
                   .sort_values("late_pct", ascending=False)
                   .head(10))

print("Top 10 Worst Suppliers by Late Delivery %:")
print(supplier_perf.to_string())

# ── 2. Slow-moving inventory ───────────────────────────────────────────────────
df["days_on_hand"] = df["stock_on_hand"] / df["avg_daily_demand"].replace(0, np.nan)

def classify(d):
    if pd.isna(d):    return "Dead Stock"
    if d > 90:        return "Slow Moving"
    if d > 45:        return "Watch"
    return "Healthy"

df["status"] = df["days_on_hand"].apply(classify)
print("\nInventory Status Breakdown:")
print(df["status"].value_counts())

# ── 3. Reorder Point Model ────────────────────────────────────────────────────
# Formula: ROP = avg_daily_demand × lead_time + safety_stock
# Safety stock = 1.645 × demand_std × √(lead_time)   [95% service level]

Z = 1.645

sku = (df.groupby("product_id")
         .agg(avg_demand=("avg_daily_demand","mean"),
              demand_std=("demand_std_dev","mean"),
              avg_lead_time=("actual_lead_time_days","mean"))
         .reset_index())

sku["safety_stock"]  = (Z * sku["demand_std"] * np.sqrt(sku["avg_lead_time"])).round(0)
sku["reorder_point"] = (sku["avg_demand"] * sku["avg_lead_time"] + sku["safety_stock"]).round(0)

print(f"\nReorder Points Calculated for {len(sku):,} SKUs")
print(sku[["product_id","avg_demand","avg_lead_time","safety_stock","reorder_point"]].head(10).to_string(index=False))

# ── 4. Simple Charts ──────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
fig.suptitle("Supply Chain Analysis", fontsize=13, fontweight="bold")

# Late delivery by category
late_by_cat = df.groupby("category")["is_late"].mean() * 100
late_by_cat.sort_values().plot(kind="barh", ax=axes[0], color="#0F3460")
axes[0].set_title("Late Delivery Rate by Category (%)")
axes[0].set_xlabel("% Orders Late")

# Inventory status breakdown
df["status"].value_counts().plot(kind="bar", ax=axes[1],
    color=["#2ECC71","#F5A623","#E94560","#95A5A6"])
axes[1].set_title("Inventory Health Status")
axes[1].set_xlabel("")
axes[1].tick_params(axis="x", rotation=30)

plt.tight_layout()
plt.savefig("visuals/supply_chain_analysis.png", dpi=150)
plt.show()
print("\nChart saved to visuals/supply_chain_analysis.png")

# Supply Chain & Inventory Optimization

**Tools:** Python · SQL · Tableau  
**Dataset:** 180,000+ row supply chain dataset

---

## What I Did

### 1. Found the problem suppliers (SQL)
Queried order and shipment data to find which suppliers were consistently delivering late and had high defect rates.

### 2. Flagged slow-moving inventory (SQL + Python)
Calculated how many days of stock each product had sitting in the warehouse. Anything with too many days on hand was flagged for review.

### 3. Modeled better reorder points (Python)
Used average demand and lead time data to calculate when to reorder each product — so we're not running out of stock or over-ordering.  
**Result:** Projected ~18% reduction in stockout risk.

### 4. Built a Tableau dashboard
Tracked supplier lead times, defect rates, and fulfillment performance by region — all in one place for the ops team.

---

## File Structure

```
├── data/
│   └── sample_data.csv        # Sample of the dataset
├── sql/
│   ├── slow_moving_inventory.sql
│   └── supplier_performance.sql
├── notebooks/
│   └── analysis.py            # EDA + reorder point model
└── README.md
```

---

## Key Takeaways
- Identified bottleneck suppliers driving ~30% of late deliveries
- Flagged ~12% of SKUs as slow-moving, contributing to excess holding costs
- Reorder point model reduced estimated stockout risk by 18% vs. existing thresholds

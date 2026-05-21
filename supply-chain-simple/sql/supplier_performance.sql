-- Supplier Performance: Find suppliers with late deliveries and high defect rates

SELECT
    supplier_id,
    supplier_name,
    COUNT(order_id)                                                      AS total_orders,
    ROUND(AVG(actual_lead_time - promised_lead_time), 1)                 AS avg_delay_days,
    ROUND(AVG(defect_rate_pct), 2)                                       AS avg_defect_rate,
    ROUND(100.0 * SUM(CASE WHEN actual_lead_time > promised_lead_time
                           THEN 1 ELSE 0 END) / COUNT(order_id), 1)     AS late_delivery_pct

FROM orders
JOIN suppliers USING (supplier_id)
WHERE order_date >= CURRENT_DATE - INTERVAL '12 months'
GROUP BY supplier_id, supplier_name
HAVING COUNT(order_id) >= 10
ORDER BY avg_delay_days DESC;

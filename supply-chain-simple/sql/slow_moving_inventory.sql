-- Slow-Moving Inventory: Flag products with too many days of stock on hand

SELECT
    product_id,
    product_name,
    category,
    stock_on_hand,
    avg_daily_demand,
    ROUND(stock_on_hand / NULLIF(avg_daily_demand, 0), 0) AS days_on_hand,

    CASE
        WHEN avg_daily_demand = 0                                          THEN 'Dead Stock'
        WHEN stock_on_hand / avg_daily_demand > 90                        THEN 'Slow Moving'
        WHEN stock_on_hand / avg_daily_demand > 45                        THEN 'Watch'
        ELSE                                                                    'Healthy'
    END AS status

FROM inventory
ORDER BY days_on_hand DESC;

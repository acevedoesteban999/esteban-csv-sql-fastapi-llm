DROP VIEW IF EXISTS sales_by_month_country;
CREATE VIEW sales_by_month_country AS
SELECT
    strftime('%Y-%m', order_date) AS month,
    country,
    COUNT(*)                      AS orders,
    ROUND(SUM(amount), 2)         AS total_sales
FROM orders
WHERE status = 'completed'
GROUP BY month, country;

DROP VIEW IF EXISTS top_10_customers;
CREATE VIEW top_10_customers AS
SELECT
    customer,
    COUNT(*)              AS orders,
    ROUND(SUM(amount), 2) AS total_spent
FROM orders
WHERE status = 'completed'
GROUP BY customer
ORDER BY total_spent DESC
LIMIT 10;
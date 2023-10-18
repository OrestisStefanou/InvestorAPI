SELECT AVG(sts.close_price), substr(sts.registered_date, 4, 7) AS month_year , sts.registered_date
FROM stock_time_series as sts
INNER JOIN stock_overview as so
ON sts.symbol = so.symbol
WHERE so.sector = 'ENERGY & TRANSPORTATION' AND sts.registered_date_ts > strftime('%s', '2018-01-01')
GROUP BY month_year
ORDER BY sts.registered_date_ts ASC

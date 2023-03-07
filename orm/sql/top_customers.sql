SELECT 
	c.id, 
	c.first_name, 
	SUM(i.total) AS total
FROM Invoice i 
LEFT JOIN Customer c ON i.customer_id = c.id
GROUP BY c.id, c.first_name
ORDER BY total DESC
LIMIT :limit;
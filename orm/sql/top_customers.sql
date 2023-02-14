SELECT 
	c.CustomerId, 
	c.FirstName, 
	SUM(i.Total) AS Total
FROM Invoice i 
LEFT JOIN Customer c ON i.CustomerId = c.CustomerId
GROUP BY c.CustomerId, c.FirstName
ORDER BY TOTAL DESC
LIMIT {{number_of_top_customers}};
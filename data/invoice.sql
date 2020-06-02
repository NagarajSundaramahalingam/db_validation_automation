-- To check invoice date > 2021 

SELECT 
	*
FROM 
	Invoice
WHERE
	invoice_date < '1/1/2021';
WITH cte_rank AS
(
	SELECT 
	d.name AS Department, 
	e.name AS Employee, 
	e.salary AS Salary,
	DENSE_RANK() OVER (
		PARTITION BY d.name
		ORDER BY e.salary DESC
		) AS salary_rank
	FROM Employee AS e 
	INNER JOIN Department AS d
	ON d.id= e.departmentId
)
SELECT
	Department, 
  	Employee, 
  	Salary
FROM
	cte_rank 
WHERE
	salary_rank<= 3
ORDER BY
	Department,
	Salary DESC,
	Employee;
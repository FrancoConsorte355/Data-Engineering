---CTE de mejores vendedores, vendedores que mas generan ingresos
WITH vendedor_top as (
		SELECT          SalesPersonID,
                        SUM(TotalPrice) as Ingreso_Generado
                        FROM sales
                        GROUP BY SalesPersonID
                        )
	 SELECT 
			vt.SalesPersonID,
            vt.Ingreso_Generado,
            e.FirstName,
            e.LastName
	 FROM vendedor_top AS vt
     JOIN employees as e
     ON vt.SalesPersonID = e.EmployeeID
     ORDER BY Ingreso_Generado DESC
     LIMIT 5;
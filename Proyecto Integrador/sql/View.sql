-- CREAR UNA VISTA QUE INDICA EL INGRESO POR MES
CREATE VIEW ventas_total_mes AS
SELECT
  YEAR(SalesDate)  AS Año,
  MONTH(SalesDate) AS Mes,
  SUM(TotalPrice)  AS TotalMensual
FROM sales
GROUP BY
  YEAR(SalesDate),
  MONTH(SalesDate);
  
SELECT * FROM ventas_total_mes
ORDER BY Mes ASC;
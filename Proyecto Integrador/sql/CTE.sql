---Con una función de ventana, promedio de ventas por categoria sin perder el detalle por fila
WITH ventas_con_categoria AS (
  SELECT
    s.SalesID,
    s.ProductID,
    p.CategoryID,
    s.TotalPrice
  FROM sales AS s
  INNER JOIN products AS p
    ON s.ProductID = p.ProductID
)
SELECT
  v.SalesID,
  v.ProductID,
  v.CategoryID,
  v.TotalPrice,
  AVG(v.TotalPrice) 
    OVER (PARTITION BY v.CategoryID) AS PrecioPromedioXCategoria
FROM ventas_con_categoria AS v
LIMIT 5;

---CTE de mejores vendedores, vendedores que mas generan ingresos
WITH vendedor_top AS (
    SELECT
        SalesPersonID,
        SUM(TotalPrice) AS Ingreso_Generado
    FROM sales
    GROUP BY SalesPersonID
)
SELECT
    vt.SalesPersonID,
    vt.Ingreso_Generado,
    e.FirstName,
    e.LastName
FROM vendedor_top AS vt
  INNER JOIN employees AS e
    ON vt.SalesPersonID = e.EmployeeID
ORDER BY vt.Ingreso_Generado DESC
LIMIT 5;


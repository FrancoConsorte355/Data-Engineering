---Funcion de ventana, RowNum que asigna un número secuencial a cada fila, ordenadas primero por Año y luego por Mes
SELECT
  Año,
  Mes,
  TotalMensual,
  ROW_NUMBER() OVER (
    ORDER BY Año, Mes
  ) AS RowNum
FROM ventas_total_mes;




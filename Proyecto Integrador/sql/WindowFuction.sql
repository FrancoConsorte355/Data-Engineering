---Funcion de ventana, RowNum que asigna un número secuencial a cada fila según el ingreso del mes (TotalMensual), ordenadas primero por Año y luego por Mes. 
---Como extra se añadio el crecimiento (o caida) con respecto al mes anterior
WITH ventas_base AS (
    SELECT
      Año,
      Mes,
      TotalMensual,
      LAG(TotalMensual) OVER (
        PARTITION BY Año 
        ORDER BY Mes
      ) AS TotalAnterior
    FROM ventas_total_mes
)
SELECT
  vb.Año,
  vb.Mes,
  vb.TotalMensual,
  vb.TotalAnterior,
  CASE
    WHEN vb.TotalAnterior IS NULL
      THEN NULL
    ELSE
      ROUND(
        (vb.TotalMensual - vb.TotalAnterior)
        / vb.TotalAnterior
        * 100
      , 2)
  END AS CrecimientoPct,
  ROW_NUMBER() OVER (
    ORDER BY vb.TotalMensual DESC
  ) AS RowNum
FROM ventas_base AS vb
ORDER BY vb.Año, vb.Mes;

# Proyecto Integrador

---

## Tabla de Contenidos

- [Misión](#misión)
- [Avance 1](#avance-1)
  - [Estructura del Proyecto](#estructura-del-proyecto)
  - [Preparación del Entorno Virtual](#preparación-del-entorno-virtual)
  - [Dependencias](#dependencias-requirementstxt)
  - [Ejecución de la Aplicación](#ejecución-de-la-aplicación)
  - [Manejo de Errores en la Ingestión y Validación de Datos](#manejo-de-errores-en-la-ingestión-y-validación-de-datos)
- [Avance 2](#avance-2)
  - [Patrones de Diseño Implementados](#patrones-de-diseño-implementados)
  - [Exportación de `run_sql`](#exportación-de-run_sql--dbrun_sql-archivo-srcdbpy)
  - [Pruebas Unitarias con pytest](#pruebas-unitarias-con-pytest)
  - [Seguridad con .env](#seguridad-con-env)
  - [Notebook de Integración (avance_2.ipynb)](#notebook-de-integración-anvance_2ipynb)
- [Avance 3](#avance-3)
  - [Notebook de Integración (avance_3.ipynb)](#notebook-de-integración-anvance_3ipynb)
  - [Buenas Prácticas y Optimización de Consultas](#buenas-practicas-y-optimizacion-de-consultas)

---

## Misión

Diseñar e implementar un sistema robusto que:

- Procese datos de ventas a partir de archivos CSV.
- Almacene la información en una base de datos relacional (MySQL).
- Permita análisis avanzados mediante consultas SQL.
- Modele la lógica en Python empleando Programación Orientada a Objetos.
- Aplique patrones de diseño para mejorar la escalabilidad y mantenibilidad del software.

---
# Avance 1

## Estructura del Proyecto

```plaintext
├── data
│   ├── raw                     # Archivos fuente (.csv, .json)
│   └── processed               # Archivos transformados y listos para cargar
├── sql               
│   ├── createDB.sql           # Scripts SQL para creación de la base de datos y tablas
│   └── load_data.sql          # Scripts SQL para carga y preparación de tablas (Excepto sales)
├── src                         # Código fuente
│   ├── config.py               # Variables de entorno y configuración general
│   ├── db.py                   # Conexión y sesión con la base de datos MySQL
│   ├── ingestion               # Lectura de archivos y carga en memoria
│   │   └── lector.py
│   ├── models                  # Definición de entidades y mapeo ORM
│   │   ├── categories.py
│   │   ├── cities.py
│   │   ├── countries.py
│   │   ├── customers.py
│   │   ├── employees.py
│   │   ├── products.py
│   │   └── sales.py
│   ├── processing               # Lógica de transformación y gestión de ventas
│   │   └── sales_manager.py
│   └── tests                    # Pruebas unitarias con pytest
├── venv                         # Entorno virtual (no versionar)
├── .env                         # Variables de entorno (credenciales, configuraciones)
├── requirements.txt             # Lista de dependencias del proyecto
├── run_pipeline.py              # Script principal que orquesta la pipeline de datos
└── test_db_connection.py        # Verificación de conectividad a la base de datos
```

---

## Preparación del Entorno Virtual

1. Crear y activar el entorno:

   ```bash
   python -m venv venv
   # Windows PowerShell
   .\venv\Scripts\Activate.ps1
   # Windows CMD
   .\venv\Scripts\activate.bat
   # macOS / Linux
   source venv/bin/activate
   ```

2. Instalar dependencias:

   ```bash
   pip install -r requirements.txt
   ```

---

## Dependencias (`requirements.txt`)

<details>
<summary>Ver lista de dependencias</summary>

- asttokens==3.0.0
- colorama==0.4.6
- comm==0.2.2
- debugpy==1.8.14
- decorator==5.2.1
- executing==2.2.0
- greenlet==3.2.2
- iniconfig==2.1.0
- ipykernel==6.29.5
- ipython==9.2.0
- ipython_pygments_lexers==1.1.1
- jedi==0.19.2
- jupyter_client==8.6.3
- jupyter_core==5.8.1
- matplotlib-inline==0.1.7
- mysql-connector-python==9.3.0
- nest-asyncio==1.6.0
- numpy==2.2.6
- packaging==25.0
- pandas==2.2.3
- parso==0.8.4
- platformdirs==4.3.8
- pluggy==1.6.0
- prompt_toolkit==3.0.51
- psutil==7.0.0
- pure_eval==0.2.3
- Pygments==2.19.1
- pytest==8.3.5
- python-dateutil==2.9.0.post0
- python-decouple==3.8
- python-dotenv==1.1.0
- pytz==2025.2
- pywin32==310
- pyzmq==26.4.0
- six==1.17.0
- SQLAlchemy==2.0.41
- stack-data==0.6.3
- tornado==6.5.1
- traitlets==5.14.3
- typing_extensions==4.13.2
- tzdata==2025.2
- wcwidth==0.2.13

</details>

---

## Ejecución de la Aplicación

Con el entorno virtual activo, en la raíz del proyecto:

```bash
python run_pipeline.py
```

Durante la ejecución, la pipeline:

- Procesará los archivos CSV desde `data/raw`.
- Mostrará un `head()` de los datos cargados.
- Informará conteo de valores nulos y tipos de datos por columna.
- Indicará uso de memoria y tiempos parciales de archivado, procesamiento y total.
- Al concluir, mostrará un resumen de tiempos y un mensaje de "Pipeline completada".
- Los datos de "sales" son cargados correctamente a la base de datos en MySQL.

---

## Manejo de Errores en la Ingestión y Validación de Datos

Este documento describe los mecanismos implementados para gestionar errores durante la **ingestión y validación de archivos** dentro del sistema, asegurando una ejecución robusta y proporcionando mensajes de error claros al usuario.

### 1. Verificación de existencia/permisos de carpeta

- En el constructor de `LectorDatos`, se envuelve `os.makedirs` en un bloque `try/except` para manejar errores de permiso o rutas inválidas.
- En caso de fallo, se lanza `RuntimeError` con información detallada sobre el problema al crear o leer la carpeta.

### 2. Manejo de errores en `listar_archivos`

## Manejo de Errores en la Ingestión y Validación de Datos

Este documento describe los mecanismos implementados para gestionar errores durante la **ingestión y validación de archivos** dentro del sistema, asegurando una ejecución robusta y proporcionando mensajes de error claros al usuario.

---
##  1. Verificación de existencia/permisos de carpeta
- En el constructor de `LectorDatos`, se envuelve `os.makedirs` en un bloque `try/except` para **manejar errores de permiso o rutas inválidas**.
- En caso de fallo, se lanza `RuntimeError` con información detallada sobre el problema al crear o leer la carpeta.

##  2. Manejo de errores en `listar_archivos`
- Se capturan excepciones específicas:
  - `FileNotFoundError` → Si la carpeta no existe.
  - `PermissionError` → Si el usuario no tiene permisos de lectura.
  - `Exception` (genérico) → Para errores inesperados.

- Cada error incluye un mensaje claro indicando:
  - Qué carpeta se intentó acceder.
  - Por qué falló la operación.

### 3. Manejo de errores en `cargar`

- Se comprueba la existencia del archivo con `os.path.isfile`. Si no existe, se lanza `FileNotFoundError`.
- Validación de extensión: Se restringe la carga solo a `.csv` o `.json`, lanzando `ValueError` si la extensión no es válida.
- Gestión de errores específicos en `pd.read_csv` y `pd.read_json`:
  - `EmptyDataError / ValueError` → Si el formato es incorrecto o corrupto.
  - `PermissionError` → Si el usuario no tiene permisos de acceso.
  - `Exception` → Para errores inesperados.
- Conversión de columna `fecha`:
  - Si existe, se intenta transformar a `datetime`.
  - Si la conversión falla, se imprime una advertencia (`⚠️ Advertencia`), pero no se bloquea la carga del archivo.

### 4. Validación de extensión en `LectorFactory`

- Se verifica que el argumento de extensión no sea vacío ni `None` antes de compararlo.
- Se proporciona un mensaje de error detallado con las extensiones admitidas (`.csv` y `.json`).

### 5. Mensajes claros y consistentes

Cada excepción está diseñada para proporcionar información precisa al usuario, asegurando transparencia en los errores detectados. Se reportan los siguientes casos:

- La carpeta de datos no existe o no se pudo crear.
- Un archivo concreto no está presente en el directorio.
- La extensión del archivo no es válida (debe ser `.csv` o `.json`).
- El archivo tiene formato incorrecto (JSON mal formado, CSV corrupto, etc.).
- Falta de permisos para acceder al sistema de archivos.

- **Cada error incluye un mensaje claro** indicando:
  - Qué carpeta se intentó acceder.
  - Por qué falló la operación.

##  3. Manejo de errores en `cargar`
- Se comprueba la **existencia del archivo** con `os.path.isfile`. Si no existe, se lanza `FileNotFoundError`.
- **Validación de extensión**: Se restringe la carga solo a `.csv` o `.json`, lanzando `ValueError` si la extensión no es válida.
- **Gestión de errores específicos** en `pd.read_csv` y `pd.read_json`:
  - `EmptyDataError / ValueError` → Si el formato es incorrecto o corrupto.
  - `PermissionError` → Si el usuario no tiene permisos de acceso.
  - `Exception` → Para errores inesperados.
- **Conversión de columna `fecha`**:
  - Si existe, se intenta transformar a `datetime`.
  - Si la conversión falla, se imprime una **advertencia** (`⚠️ Advertencia`), pero no se bloquea la carga del archivo.

##  4. Validación de extensión en `LectorFactory`
- Se verifica que el **argumento de extensión** no sea vacío ni `None` antes de compararlo.
- Se proporciona un **mensaje de error detallado** con las **extensiones admitidas** (`.csv` y `.json`).

##  5. Mensajes claros y consistentes
Cada excepción está diseñada para proporcionar información precisa al usuario, asegurando transparencia en los errores detectados. Se reportan los siguientes casos:
- La carpeta de datos no existe** o no se pudo crear.  
- Un archivo concreto no está presente** en el directorio.  
- La extensión del archivo no es válida** (debe ser `.csv` o `.json`).  
- El archivo tiene formato incorrecto** (JSON mal formado, CSV corrupto, etc.).  
- Falta de permisos para acceder al sistema de archivos.  

---

# Avance 2

## Patrones de Diseño Implementados

### 1. Singleton (`src/db.py`)

- **Funcionalidad:**  
  El patrón Singleton asegura que exista una única instancia de la clase `Database` en toda la aplicación.
  - En `Database.__new__()` se verifica si ya existe una instancia almacenada en `Database._instance`.
  - Si no existe, se crea, se invoca `_setup()` para inicializar el `engine`, la fábrica de sesiones (`SessionLocal`) y la base declarativa (`Base`).
  - Todas las llamadas posteriores a `Database()` devuelven la misma instancia compartida.

- **Beneficios:**
  1. Uso único de recursos: Se evitan múltiples conexiones innecesarias a la base de datos y se optimiza el pool de conexiones.
  2. Configuración centralizada: Cualquier cambio en la configuración se hace en un solo lugar.
  3. Evita inconsistencias: Siempre se instancia el mismo objeto.
=======
- **Beneficios**:  
  1. **Uso único de recursos**: Al reutilizar el mismo `engine` y las mismas configuraciones de conexión, se evitan múltiples conexiones innecesarias a la base de datos y se optimiza el pool de conexiones.  
  2. **Configuración centralizada**: Cualquier cambio en la URL de conexión, pool de conexiones o parámetros de SQLAlchemy se hace en un solo lugar, y todas las partes del sistema usan esa misma configuración.  
  3. **Evita inconsistencias**: No existe el riesgo de tener instancias duplicadas apuntando a URIs o credenciales diferentes, porque siempre se instancia el mismo objeto.

---

### 2. Builder (`src/models/sales.py`)

- **Funcionalidad:**  
  El patrón Builder permite crear instancias de la entidad `Sales` paso a paso.
  - Se expone `Sales.builder()` que devuelve un `SalesBuilder`.
  - `SalesBuilder` cuenta con métodos `set_*` para asignar cada uno de los campos de `Sales`.
  - Una vez establecidos todos los campos obligatorios, se llama a `.build()` para validar y devolver la instancia de `Sales`. Si falta algún campo obligatorio, `build()` lanza `ValueError`.

- **Beneficios:**
  1. Fácil extensión: Agregar nuevos campos no requiere modificar el constructor original.
  2. Separación de responsabilidades: La lógica de construcción queda aislada en `SalesBuilder`.
  3. Lectura clara y encadenada: El código es más legible y mantenible.

---

### 3. Factory Method (`src/ingestion/lector.py`)

- **Funcionalidad:**  
  Permite seleccionar dinámicamente el lector adecuado según la extensión del archivo de entrada (CSV o JSON).
  - En `LectorFactory.get_lector(ext)`, se recibe la extensión del archivo.
  - Si la extensión es `.csv`, devuelve una instancia de `LectorCSV`; si es `.json`, devuelve una instancia de `LectorJSON`.
  - En caso de una extensión distinta, lanza `ValueError`.

- **Beneficios:**
  1. Extensibilidad sencilla: Agregar soporte para nuevos formatos es simple.
  2. Separación de responsabilidades: Cada clase concreta se encarga de su propio formato.
  3. Código desacoplado y fácil de mantener.

- **Beneficios**:  
  1. **Fácil extensión**: Si en el futuro se añade un campo nuevo a la tabla `sales` (por ejemplo `payment_method`, `promo_code`, etc.), basta con agregar un método `set_payment_method(...)` en `SalesBuilder` sin modificar el constructor original de `Sales`. El consumidor del Builder no se ve obligado a cambiar la firma de `Sales(...)`.  
  2. **Separación de responsabilidades**: La lógica de construcción (validación de campos, valores por defecto, etc.) queda aislada en `SalesBuilder`, mientras que la clase `Sales` se mantiene limpia, con solo mapeo ORM y su propia lógica de negocio (por ejemplo `calcular_total()`).  
  3. **Lectura clara y encadenada**: El código que crea ventas en el pipeline queda más legible, al encadenar `builder.set_...().set_...().build()` en lugar de pasar un montón de parámetros posicionales o diccionarios sueltos.

### 3. Factory Method (archivo src/ingestion/lector.py)
- **Funcionalidad**:
  El patrón Factory Method permite seleccionar dinámicamente el lector adecuado según la extensión del archivo de entrada (CSV o JSON).
   - En LectorFactory.get_lector(ext), se recibe la extensión del archivo (.csv o .json).
   - Si la extensión es .csv, devuelve una instancia de LectorCSV; si es .json, devuelve una instancia de LectorJSON.
   - En caso de una extensión distinta, lanza ValueError indicando que el formato no está soportado.

- **Beneficios**: 
   1. **Extensibilidad sencilla**: Para soportar un nuevo formato (por ejemplo, XML), basta con agregar una clase LectorXML y extender get_lector() para reconocer .xml, sin modificar la lógica de carga existente.
   2. **Separación de responsabilidades**: La lógica de “qué lector usar” queda centralizada en LectorFactory, mientras que cada clase concreta (LectorCSV o LectorJSON) solo se encarga de leer y parsear su propio formato.
   3. **Código desacoplado y fácil de mantener**: Los módulos que consumen archivos (por ejemplo, la pipeline) solo llaman a get_lector(ext) sin preocuparse por detalles internos de lectura. Si en el futuro cambian los requisitos de validación de un formato, solo se ajusta la clase específica, sin tocar el resto de la aplicación.

---

## Exportación de `run_sql = db.run_sql` (archivo `src/db.py`)

- **Qué es:**  
  Método interno `Database.run_sql(sql: str, params: dict = None) -> pandas.DataFrame` que:
  1. Abre una conexión (`self.engine.connect()`).
  2. Llama a `pd.read_sql_query(sql, conn, params)` para ejecutar la consulta y obtener un DataFrame.
  3. Devuelve ese DataFrame con el resultado de la query.

- **Cómo se usa:**

  ```python
  from src.db import run_sql

  df = run_sql(
      "SELECT CustomerID, COUNT(*) AS total_sales FROM sales GROUP BY CustomerID",
      params=None
  )
  print(df.head())
  ```

---

## Pruebas Unitarias con pytest

Se implementaron dos archivos de prueba en la carpeta `tests/`, usando pytest:

1. **tests/test_singleton_db.py**
   - Verifica que `Database()` devuelva siempre la misma instancia (Singleton).
   - Comprueba que la instancia global `db` es idéntica a `Database()`.
   - Asegura que `engine` y `SessionLocal` sean objetos únicos compartidos.

2. **tests/test_sales_builder.py**
   - Prueba que, usando `SalesBuilder` y definiendo todos los campos obligatorios, se construya correctamente un objeto `Sales`.
   - Verifica que, al omitir cualquier campo obligatorio, `builder.build()` lance `ValueError`.

**Cómo ejecutar las pruebas:**

```bash
pytest -q
```

Pytest buscará automáticamente los archivos `test_*.py` en `tests/` y emitirá un reporte con PASSED o FAILED para cada caso.

---

## Seguridad con .env

**Propósito:** Gestionar credenciales sensibles de conexión.

**Ejemplo de `.env`:** (no son datos reales)

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=1234
DB_NAME=proyecto_integrador
```

**Protección:**

- Se carga con `python-decouple`.
- Se excluye del repositorio (`.gitignore`).
- Se recomienda un `.env.example` sin datos reales.
=======
## Notebook de Integración (anvance_2.ipynb)
## Propósito: Documentar la conexión, consultas SQL y pruebas unitarias en un entorno interactivo.
## Incluye:
  * Validación de conexión (SELECT 1).
  * Ejecución de consultas SQL:
       * SUBCONSULTAS SIMPLES
       * SUBCONSULTAS CORRELACIONADAS
       * SUBCONSULTAS NO CORRELACIONADAS
       * CTE
       * Window Functions
  * Demostración de patrones de diseño (Singleton, Builder, Factory).
  * Ejecución de pruebas unitarias(pytest).

# Avance 3
## Notebook de Integración (anvance_3.ipynb)

Este avance contiene ejemplos prácticos de consultas SQL, procedimientos almacenados, funciones de ventana, vistas, CTEs, Indices y triggers aplicados a una base de datos de ventas. A continuación se describen las funciones y procesos implementados en cada celda, dentro de avance_3.ipynb:

---

## Notebook de Integración (`anvance_2.ipynb`)

**Propósito:** Documentar la conexión, consultas SQL y pruebas unitarias en un entorno interactivo.

**Incluye:**

- **Validación de conexión (`SELECT 1`):**  
  Verifica la conexión a la base de datos mediante la importación de `SessionLocal` desde `src.db`.

- **Ejecución de consultas SQL:**  
  Incluye subconsultas simples, subconsultas correlacionadas, CTEs y funciones de ventana, con optimizaciones e índices.

- **Demostración de patrones de diseño:**  
  Ejemplos prácticos de Singleton, Factory y Builder.

- **Ejecución de pruebas unitarias (`pytest`):**  
  Permite verificar en vivo que los patrones pasan sus pruebas sin fallos.

---

# Avance 3

## Notebook de Integración (`anvance_3.ipynb`)

Este avance contiene ejemplos prácticos de consultas SQL, procedimientos almacenados, funciones de ventana, vistas, CTEs, índices y triggers aplicados a una base de datos de ventas.

---

### 1. Mejores Vendedores (`vendedor_top`)

- **Descripción de la consulta:**  
  Utiliza una CTE para identificar los vendedores que más ingresos generan. Se agrupan las ventas por `SalesPersonID`, se suman los ingresos y se obtienen los 5 vendedores principales junto con su nombre y apellido.

- **Tiempo de procesamiento antes de la optimización:** 0.094 s  
- **Optimizaciones:**  
  - Creación y utilización de índices: `idx_sales_person_total` y de `employeeID` (clave primaria).
  - Uso de `INNER JOIN` en lugar de `LEFT JOIN`.
  - Unión de la CTE con `employees` después de agrupar.

- **Tiempo de procesamiento después de la optimización:** 0.015 s  
  - Mejora de un 84.04%

---

### 2. Ingreso por Mes (`ventas_total_mes`)

- **Descripción de la consulta:**  
  Consulta una vista que muestra el ingreso total por mes, ordenando los resultados cronológicamente.

- **Tiempo de procesamiento antes de la optimización:** 0.031 s  
- **Optimizaciones:**  
  - Creación de vista para evitar agrupaciones repetidas.
  - Uso del índice `idx_sales_salesdate`.

- **Tiempo de procesamiento después de la optimización:** 0.010 s  
  - Mejora de un 67.74%

---

### 3. Función de Ventana (`ROW_NUMBER`)

- **Descripción de la consulta:**  
  Utiliza la función de ventana `ROW_NUMBER()` para asignar un número secuencial a cada fila, ordenadas por año y mes, sobre la vista de ventas mensuales.

- **Tiempo de procesamiento antes de la optimización:** 0.047 s  
- **Optimizaciones:**  
  - Precalcular `LAG(TotalMensual)` en una CTE intermedia.
  - Utilización de índices.

- **Tiempo de procesamiento después de la optimización:** 0.031 s  
  - Mejora de un 34.04%

---

### 4. Procedimiento Almacenado (`registro_productos`)

- **Descripción de la consulta:**  
  Ejecuta un procedimiento almacenado para agregar un nuevo producto ("Chocolinas") a la base de datos.  
  Verifica si ya existe un producto con ese nombre y utiliza `SIGNAL SQLSTATE '45000'` para mostrar un mensaje de error si corresponde.

---

### 5. Trigger de Seguridad (`TotalPrice`)

- **Descripción de la consulta:**  
  Trigger que valida que el campo `TotalPrice` en la tabla de ventas sea igual a `Quantity * Precio - Discount`.  
  Si la validación falla, se genera un error para evitar registros incorrectos.

---

### 6. Índices

- **Descripción:**  
  Se muestra la creación de índices en la carpeta `sql`:
    - Por fecha: `idx_sales_salesdate`
    - Por producto: `idx_sales_productid`
    - Por categoría y precio: `idx_products_category_price`
    - Por producto y precio total: `idx_sales_productid_totalprice`
    - Por vendedor y precio total: `idx_sales_person_total`

---

## Variables Importantes

- **df_customers:** DataFrame de pandas que almacena los resultados de las consultas SQL.
- **query:** Variable tipo string que contiene las sentencias SQL utilizadas.

---

## Buenas Prácticas y Optimización de Consultas

Las consultas realizadas siguen pautas para optimización y velocidad en caso de escalabilidad del sistema:

- Joins explícitos
- Agrupación mínima y necesaria
- Eliminación de subconsultas innecesarias
- Evitar funciones de alto costo computacional
- Creación de índices para las diferentes tablas

---


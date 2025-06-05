# Proyecto Integrador

## Misión

Diseñar e implementar un sistema robusto que:

* Procese datos de ventas a partir de archivos CSV.
* Almacene la información en una base de datos relacional (MySQL).
* Permita análisis avanzados mediante consultas SQL.
* Modele la lógica en Python empleando Programación Orientada a Objetos.
* Aplique patrones de diseño para mejorar la escalabilidad y mantenibilidad del software.

## Avance 1

## Estructura del Proyecto

```
├── data
│   ├── raw           # Archivos fuente (.csv, .json)
│   └── processed     # Archivos transformados y listos para cargar
├── sql               # Scripts SQL para carga y preparación de tablas
│   └── load_data.sql
├── src               # Código fuente
│   ├── config.py     # Variables de entorno y configuración general
│   ├── db.py         # Conexión y sesión con la base de datos MySQL
│   ├── ingestion     # Lectura de archivos y carga en memoria
│   │   └── lector.py
│   ├── models        # Definición de entidades y mapeo ORM
│   │   ├── categories.py
│   │   ├── cities.py
│   │   ├── countries.py
│   │   ├── customers.py
│   │   ├── employees.py
│   │   ├── products.py
│   │   └── sales.py
│   ├── processing    # Lógica de transformación y gestión de ventas
│   │   └── sales_manager.py
│   └── tests         # Pruebas unitarias con pytest
├── venv              # Entorno virtual (no versionar)
├── .env              # Variables de entorno (credenciales, configuraciones)
├── requirements.txt  # Lista de dependencias del proyecto
├── run_pipeline.py   # Script principal que orquesta la pipeline de datos
└── test_db_connection.py  # Verificación de conectividad a la base de datos
```

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

## Dependencias (requirements.txt)

* asttokens==3.0.0
* colorama==0.4.6
* comm==0.2.2
* debugpy==1.8.14
* decorator==5.2.1
* executing==2.2.0
* greenlet==3.2.2
* iniconfig==2.1.0
* ipykernel==6.29.5
* ipython==9.2.0
* ipython_pygments_lexers==1.1.1
* jedi==0.19.2
* jupyter_client==8.6.3
* jupyter_core==5.8.1
* matplotlib-inline==0.1.7
* mysql-connector-python==9.3.0
* nest-asyncio==1.6.0
* numpy==2.2.6
* packaging==25.0
* pandas==2.2.3
* parso==0.8.4
* platformdirs==4.3.8
* pluggy==1.6.0
* prompt_toolkit==3.0.51
* psutil==7.0.0
* pure_eval==0.2.3
* Pygments==2.19.1
* pytest==8.3.5
* python-dateutil==2.9.0.post0
* python-decouple==3.8
* python-dotenv==1.1.0
* pytz==2025.2
* pywin32==310
* pyzmq==26.4.0
* six==1.17.0
* SQLAlchemy==2.0.41
* stack-data==0.6.3
* tornado==6.5.1
* traitlets==5.14.3
* typing_extensions==4.13.2
* tzdata==2025.2
* wcwidth==0.2.13


## Ejecución de la Aplicación

Con el entorno virtual activo, en la raíz del proyecto:

```bash
python run_pipeline.py
```

Durante la ejecución la pipeline:

* Procesará los archivos CSV desde `data/raw`.
* Mostrará un `head()` de los datos cargados.
* Informará conteo de valores nulos y tipos de datos por columna.
* Indicará uso de memoria y tiempos parciales de archivado, procesamiento y total.
* Al concluir, mostrará un resumen de tiempos y un mensaje de "Pipeline completada".
* Los datos de "sales", son cargados de manera correcta a la base de datos en MySQL.

# Manejo de Errores en la Ingestión y Validación de Datos

Este documento describe los mecanismos implementados para gestionar errores durante la **ingestión y validación de archivos** dentro del sistema, asegurando una ejecución robusta y proporcionando mensajes de error claros al usuario.

---

##  1. Verificación de existencia/permisos de carpeta
- En el constructor de `LectorDatos`, se envuelve `os.makedirs` en un bloque `try/except` para **manejar errores de permiso o rutas inválidas**.
- En caso de fallo, se lanza `RuntimeError` con información detallada sobre el problema al crear o leer la carpeta.

---

##  2. Manejo de errores en `listar_archivos`
- Se capturan excepciones específicas:
  - `FileNotFoundError` → Si la carpeta no existe.
  - `PermissionError` → Si el usuario no tiene permisos de lectura.
  - `Exception` (genérico) → Para errores inesperados.
- **Cada error incluye un mensaje claro** indicando:
  - Qué carpeta se intentó acceder.
  - Por qué falló la operación.

---

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

---

##  4. Validación de extensión en `LectorFactory`
- Se verifica que el **argumento de extensión** no sea vacío ni `None` antes de compararlo.
- Se proporciona un **mensaje de error detallado** con las **extensiones admitidas** (`.csv` y `.json`).

---

## 🛠️ 5. Mensajes claros y consistentes
Cada excepción está diseñada para proporcionar información precisa al usuario, asegurando transparencia en los errores detectados. Se reportan los siguientes casos:
 **La carpeta de datos no existe** o no se pudo crear.  
 **Un archivo concreto no está presente** en el directorio.  
 **La extensión del archivo no es válida** (debe ser `.csv` o `.json`).  
 **El archivo tiene formato incorrecto** (JSON mal formado, CSV corrupto, etc.).  
 **Falta de permisos** para acceder al sistema de archivos.  

---

## Avance 2

## Patrones de Diseño Implementados

### 1. Singleton (archivo `src/db.py`)
- **Funcionalidad**:  
  El patrón Singleton asegura que exista una **única instancia** de la clase `Database` en toda la aplicación.  
  - En `Database.__new__()` se verifica si ya existe una instancia almacenada en `Database._instance`.  
  - Si no existe, se crea, se invoca `_setup()` para inicializar el `engine`, la fábrica de sesiones (`SessionLocal`) y la base declarativa (`Base`).  
  - Todas las llamadas posteriores a `Database()` devuelven la misma instancia compartida.

- **Por qué es escalable**:  
  1. **Uso único de recursos**: Al reutilizar el mismo `engine` y las mismas configuraciones de conexión, se evitan múltiples conexiones innecesarias a la base de datos y se optimiza el pool de conexiones.  
  2. **Configuración centralizada**: Cualquier cambio en la URL de conexión, pool de conexiones o parámetros de SQLAlchemy se hace en un solo lugar, y todas las partes del sistema usan esa misma configuración.  
  3. **Evita inconsistencias**: No existe el riesgo de tener instancias duplicadas apuntando a URIs o credenciales diferentes, porque siempre se instancia el mismo objeto.

### 2. Builder (archivo `src/models/sales.py`)
- **Funcionalidad**:  
  El patrón Builder permite crear instancias de la entidad `Sales` paso a paso.  
  - Se expone `Sales.builder()` que devuelve un `SalesBuilder`.  
  - `SalesBuilder` cuenta con métodos `set_*` (por ejemplo `set_sales_id()`, `set_customer_id()`, etc.) para asignar cada uno de los campos de `Sales`.  
  - Una vez establecidos todos los campos obligatorios, se llama a `.build()` para validar que no falte nada y devolver la instancia de `Sales`. Si falta algún campo obligatorio, `build()` lanza `ValueError` con la lista de campos faltantes.

- **Por qué es escalable**:  
  1. **Fácil extensión**: Si en el futuro se añade un campo nuevo a la tabla `sales` (por ejemplo `payment_method`, `promo_code`, etc.), basta con agregar un método `set_payment_method(...)` en `SalesBuilder` sin modificar el constructor original de `Sales`. El consumidor del Builder no se ve obligado a cambiar la firma de `Sales(...)`.  
  2. **Separación de responsabilidades**: La lógica de construcción (validación de campos, valores por defecto, etc.) queda aislada en `SalesBuilder`, mientras que la clase `Sales` se mantiene limpia, con solo mapeo ORM y su propia lógica de negocio (por ejemplo `calcular_total()`).  
  3. **Lectura clara y encadenada**: El código que crea ventas en el pipeline queda más legible, al encadenar `builder.set_...().set_...().build()` en lugar de pasar un montón de parámetros posicionales o diccionarios sueltos.

---

## Exportación de `run_sql = db.run_sql` (archivo `src/db.py`)

- **Qué es**:  
  Se define un método interno `Database.run_sql(sql: str, params: dict = None) -> pandas.DataFrame` que:
  1. Abre una conexión (`self.engine.connect()`).
  2. Llama a `pd.read_sql_query(sql, conn, params)` para ejecutar la consulta y obtener un DataFrame.
  3. Devuelve ese DataFrame con el resultado de la query.

- **Cómo se usa**:  
  ```python
  from src.db import run_sql

  df = run_sql(
      "SELECT CustomerID, COUNT(*) AS total_sales FROM sales GROUP BY CustomerID",
      params=None
  )
  print(df.head())

## Pruebas Unitarias con pytest
### Se implementaron dos archivos de prueba en la carpeta tests/, usando pytest:

 1. tests/test_singleton_db.py

      * Verifica que Database() devuelva siempre la misma instancia (Singleton).
      * Comprueba que la instancia global db es idéntica a Database()
      * Asegura que engine y SessionLocal sean objetos únicos compartidos por todas las invocaciones.

 2. tests/test_sales_builder.py

      * Prueba que, usando SalesBuilder y definiendo todos los campos obligatorios con set_*, se construya correctamente un objeto Sales con las propiedades asignadas.
      * Verifica que, al omitir cualquier campo obligatorio, builder.build() lance ValueError mencionando los campos faltantes.

### Cómo ejecutar las pruebas
   * Desde la raíz del proyecto, con el entorno virtual activado:
```bash
pip install -r requirements.txt  # debe incluir pytest
pytest -q
```
   *Pytest buscará automáticamente los archivos test_*.py en tests/ y emitirá un reporte con PASSED o FAILED para cada caso.

## Seguridad con .env
 ### Propósito: Gestionar credenciales sensibles de conexión.
 #### Ejemplo de .env: (no son datos reales)
``` 
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=1234
DB_NAME=proyecto_integrador
```

### Protección: 
* Se carga con python-decouple.
* Se excluye del repositorio (.gitignore).
* Se recomienda un .env.example sin datos reales.

## Notebook de Integración (integracion_final.ipynb)
# Propósito: Documentar la conexión, consultas SQL y pruebas unitarias en un entorno interactivo.
# Incluye:
  * Validación de conexión (SELECT 1).
  * Ejecución de consultas SQL:
       * SUBCONSULTAS SIMPLES
       * SUBCONSULTAS CORRELACIONADAS
       * SUBCONSULTAS NO CORRELACIONADAS
       * CTE
       * Window Functions
  * Demostración de patrones de diseño (Singleton, Builder, Factory).
  * Ejecución de pruebas unitarias(pytest).


# Descripción del Notebook

Este avance contiene ejemplos prácticos de consultas SQL, procedimientos almacenados, funciones de ventana, vistas, CTEs, Indices y triggers aplicados a una base de datos de ventas. A continuación se describen las funciones y procesos implementados en cada celda, dentro de avance_3.ipynb:

---

## 1. Mejores Vendedores (`vendedor_top`)
Se utiliza una CTE (Common Table Expression) para identificar los vendedores que más ingresos generan. Se agrupan las ventas por `SalesPersonID`, se suman los ingresos y se obtienen los 5 vendedores principales junto con su nombre y apellido.

---

## 2. Ingreso por Mes (`ventas_total_mes`)
Consulta una vista que muestra el ingreso total por mes, ordenando los resultados cronológicamente.

---

## 3. Función de Ventana (`ROW_NUMBER`)
Se utiliza la función de ventana `ROW_NUMBER()` para asignar un número secuencial a cada fila, ordenadas por año y mes, sobre la vista de ventas mensuales.

---

## 4. Procedimiento Almacenado (`registro_productos`)
Se ejecuta un procedimiento almacenado llamado `registro_productos` para agregar un nuevo producto ("Chocolinas") a la base de datos de productos.

---

## 5. Verificación de Inserción
Se consulta la tabla de productos para verificar que el producto "Chocolinas" fue insertado correctamente.

---

## 6. Trigger de Seguridad (`TotalPrice`)
Se describe y prueba un trigger de seguridad que valida que el campo `TotalPrice` en la tabla de ventas sea igual a `Quantity * Precio - Discount`. Si la validación falla, se genera un error para evitar registros incorrectos o fraudulentos.

---

## 7. Index 
Se encuentra en la carpeta sql, donde se muestra la creación de un indice para la tabla Sales, el cual funciona con SalesDate y se aplica en la función de ventana para obtener de manera más rapida la tabla, y además implementando una optimización de consultas

## Variables Importantes

- **df_customers**: DataFrame de pandas que almacena los resultados de las consultas SQL ejecutadas.
- **query**: Variable tipo string que contiene las sentencias SQL utilizadas en las distintas celdas.

## Buenas practicas y optimización de consultas

Las consultas realizadas contienen una serie de pautas para la optimización y la velocidad de consultas en el caso de que el sistema escale, donde se implemento lo siguiente:
  * Joins explícitos
  * Agrupación minima y necesaria
  * Eliminación de subconsultas
  * No se agregaron funciones de alto costo (en cuanto a rendimiento)
  * Se creó un indice para la tabla Sales

---

# Proyecto Integrador

## Misión

Diseñar e implementar un sistema robusto que:

* Procese datos de ventas a partir de archivos CSV.
* Almacene la información en una base de datos relacional (MySQL).
* Permita análisis avanzados mediante consultas SQL.
* Modele la lógica en Python empleando Programación Orientada a Objetos.
* Aplique patrones de diseño para mejorar la escalabilidad y mantenibilidad del software.

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

* greenlet==3.2.2
* mysql-connector-python==9.3.0
* numpy==2.2.6
* pandas==2.2.3
* python-dateutil==2.9.0.post0
* python-decouple==3.8
* python-dotenv==1.1.0
* pytz==2025.2
* six==1.17.0
* SQLAlchemy==2.0.41
* typing\_extensions==4.13.2
* tzdata==2025.2

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


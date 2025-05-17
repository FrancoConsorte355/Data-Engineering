# Homework1: Sistema de Gestión de Usuarios

Este proyecto en Python simula un sistema de gestión de usuarios para una plataforma ficticia. Permite:

* 📋 **Registrar usuarios** (nombre, email, contraseña)
* 🔎 **Listar usuarios** registrados
* 🔍 **Buscar usuarios** por nombre
* 🗑️ **Eliminar usuarios**
* 💾 **Guardar y cargar** la lista de usuarios en archivos externos (`.json` o `.txt`)

El código está modularizado, con validaciones, entorno virtual y pruebas unitarias.

---

## 📁 Estructura de carpetas

```
project_root/              # homework1
├── venv/                  # Entorno virtual de Python
├── .env                   # Variables de entorno (rutas y secretos)
├── data/                  # Almacena datos persistentes
│   └── users.json         # Archivo JSON con usuarios
├── src/                   # Código fuente
│   ├
│   ├── storage.py         # Carga y guardado de usuarios
│   └── users.py           # Lógica de negocio de usuarios
├── tests/                 # Pruebas unitarias
│   ├
│   └── test_users.py      # Validación de email, password y registro duplicado
├── main.ipynb             # Notebook con ejemplo de ejecución
├── main1.py               # Script CLI para PowerShell / CMD
├── requirements.txt       # Dependencias del proyecto
└── README.md              # Este archivo de documentación
```

---

## 🚀 Requisitos e instalación

1. **Clonar el repositorio** y situarse en la carpeta raíz:

   ```bash
   git clone <url-del-repo>
   cd homework1
   ```
2. **Crear y activar** entorno virtual:

   ```bash
   python -m venv venv
   # Windows PowerShell:
   .\venv\Scripts\Activate.ps1
   # Windows CMD:
   .\venv\Scripts\activate.bat
   # macOS / Linux:
   source venv/bin/activate
   ```
3. **Instalar dependencias**:

   ```bash
   pip install -r requirements.txt
   ```
4. **Configurar** variables sensibles en `.env`:

   ```dotenv
   DATA_FILE=./data/users.json
   PASSWORD_SALT=my_super_secret_salt
   ```

---

## ▶️ Cómo ejecutar la aplicación

En la raíz del proyecto, con el entorno virtual activo:

```bash
python main1.py
```

Se desplegará un menú interactivo:

```
1) Registrar usuario
2) Listar usuarios
3) Buscar usuario por nombre
4) Eliminar usuario
5) Guardar y salir
```

---

## 🛠️ Detalles del entorno virtual y `.env`

* **`venv/`**: entorno aislado de Python (3.10+).
* **`.env`**: contiene:

  * **`DATA_FILE`**: ruta al JSON de usuarios.
  * **`PASSWORD_SALT`**: salt para hashear contraseñas.

Se cargan con `python-decouple` o `python-dotenv`.

---

## 📦 Dependencias (`requirements.txt`)

```text
colorama==0.4.6
numpy==2.1.3
pandas==2.2.3
python-decouple==3.8
python-dotenv==1.1.0
```

* **`colorama`**: para colores en consola.
* **`python-decouple`** / **`python-dotenv`**: gestión de variables de entorno.

---

## 🧩 Módulos en `src/`

### `storage.py`

* `load_users() -> list[dict]`: carga usuarios desde JSON; retorna lista vacía si no existe.
* `save_users(users: list[dict]) -> None`: guarda la lista en JSON con indentación.

### `users.py`

* `hash_password(password: str) -> str`: SHA-256 + `PASSWORD_SALT`.
* `validate_email(email: str) -> bool`: regex y longitud (5–254).
* `validate_name(name: str) -> bool`: solo letras y espacios (2–50).
* `validate_password(pw: str) -> bool`: mínimo 8 caracteres, mayúscula, minúscula, dígito y símbolo.
* `register_user(users, name, email, password) -> bool`: valida, checa duplicados, hashea y agrega.
* `list_users(users) -> None`: imprime tabla de nombre y email.
* `find_users(users, query) -> list[dict]`: búsqueda case-insensitive.
* `delete_user(users, email) -> bool`: elimina por email.

---

## 📋 Scripts de ejecución

* **`main.ipynb`**: Demo en Jupyter Notebook.
* **`main1.py`**: CLI con `colorama` y manejo de errores.

  1. Carga inicial con `load_users()` y `try/except`.
  2. Menú interactivo con validaciones y mensajes en colores.
  3. Guardado final con `save_users()`.

---

## 🧪 Pruebas unitarias (`tests/test_users.py`)

* **`test_validate_email`**: casos válidos e inválidos.
* **`test_validate_password`**: contraseña válida vs inválida.
* **`test_register_user_duplicate`**: primer registro OK, segundo con email igual lanza `ValueError`.

**Ejecutar**:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

---







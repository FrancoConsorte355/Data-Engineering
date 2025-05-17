# users.py
import re
import hashlib
from decouple import config

PASSWORD_SALT = config('PASSWORD_SALT', default='')

def hash_password(password: str) -> str:   #esta funcion sirve para hashear la contraseña
    """Hashea la contraseña con SHA-256 y un salt."""
    # Usa el salt antes de hashear
    return hashlib.sha256((PASSWORD_SALT + password).encode('utf-8')).hexdigest()

def validate_email(email: str) -> bool:  #esta funcion sirve para validar el email
    """Validación básica + longitud."""
    if not (5 <= len(email) <= 254):
        return False
    # patrón básico usuario@dominio.ext
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(patron, email) is not None

def validate_name(name: str) -> bool:   #esta funcion sirve para validar el nombre
    """Solo letras y espacios; longitud entre 2 y 50."""
    if not (2 <= len(name.strip()) <= 50):
        return False
    return bool(re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$', name))

def register_user(users: list[dict], name: str, email: str, password: str) -> bool:
    """Registra un usuario si los datos son válidos y el email no existe."""
    # 1) Validaciones robustas
    if not validate_name(name):
        raise ValueError("Nombre inválido: solo letras y espacios (2–50 caracteres).")
    if not validate_email(email):
        raise ValueError("Email con formato o longitud inválida.")
    if not validate_password(password):
        raise ValueError(
            "Contraseña inválida: mínimo 8 caracteres, "
            "al menos una mayúscula, minúscula, dígito y símbolo."
        )
    # 2) Comprueba duplicados
    if any(u['email'] == email for u in users):
        raise ValueError("Ya existe un usuario con ese email.")
    # 3) Hash y registro
    users.append({
        'name':     name.strip(),
        'email':    email,
        'password': hash_password(password)
    })
    return True

def list_users(users: list[dict]) -> None:
    """Imprime en consola la lista de usuarios."""
    if not users:
        print("No hay usuarios registrados.")
        return
    print(f"{'Nombre':20} | {'Email'}")
    print("-" * 40)
    for u in users:
        print(f"{u['name']:20} | {u['email']}")

def find_users(users: list[dict], query: str) -> list[dict]:
    """Devuelve lista de usuarios cuyo nombre contiene la query (case-insensitive)."""
    q = query.lower()
    return [u for u in users if q in u['name'].lower()]

def delete_user(users: list[dict], email: str) -> bool:
    """Elimina un usuario por email. Retorna True si lo encontró."""
    for i, u in enumerate(users):
        if u['email'] == email:
            users.pop(i)
            return True
    return False

def validate_password(pw: str) -> bool:
    """Mínimo 8 caracteres, al menos mayúscula, minúscula, dígito y símbolo."""
    if len(pw) < 8:
        return False
    if not re.search(r"[A-Z]", pw):
        return False
    if not re.search(r"[a-z]", pw):
        return False
    if not re.search(r"\d", pw):
        return False
    if not re.search(r"[^\w\s]", pw):
        return False
    return True
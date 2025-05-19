# storage.py
import json
import os
from decouple import config

DATA_FILE = config('DATA_FILE', default='users.json')
PASSWORD_SALT = config('PASSWORD_SALT', default='')

def load_users() -> list[dict]:                               #usa list[dict] para indicar que es una lista de diccionarios
    """Carga la lista de usuarios desde el archivo JSON."""
    if not os.path.exists(DATA_FILE):                         #dice que si no existe la ruta al archivo lo retorna vacío
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:     #abre el archivo en modo lectura, utf-8 es el encoding de caracteres
        # Si el archivo está vacío, devuelve una lista vacía
        return json.load(f)            #carga el contenido del archivo JSON y lo convierte en una lista de diccionarios, f sirve como puntero al archivo abierto

def save_users(users: list[dict]) -> None:
    """Guarda la lista de usuarios en el archivo JSON."""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2, ensure_ascii=False)               #dump sirve para guardar el contenido de la lista de diccionarios en el archivo JSON, indent=2 es para que esté bien formateado y ensure_ascii=False es para que no convierta caracteres especiales a unicode

# storage.py
import json
import os
from decouple import config

DATA_FILE = config('DATA_FILE', default='users.json')
PASSWORD_SALT = config('PASSWORD_SALT', default='')

def load_users() -> list[dict]:
    """Carga la lista de usuarios desde el archivo JSON."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_users(users: list[dict]) -> None:
    """Guarda la lista de usuarios en el archivo JSON."""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2, ensure_ascii=False)

# 1. Configuración e imports
from dotenv import load_dotenv
load_dotenv()

from src.storage import load_users, save_users
from src.users import register_user, list_users, find_users, delete_user

from colorama import init, Fore, Style
init(autoreset=True)

# 2. Carga inicial con manejo de error
try:
    users = load_users()
except Exception as e:
    print(Fore.YELLOW + f"⚠️ Error al cargar usuarios: {e}")
    users = []

# 3. Menú de consola
def menu():
    print(Style.BRIGHT + """
    1) Registrar usuario
    2) Listar usuarios
    3) Buscar usuario por nombre
    4) Eliminar usuario
    5) Guardar y salir
    """)
    return input("Selecciona una opción: ")

while True:
    choice = menu().strip()
    try:
        if choice == '1':
            name  = input("Nombre: ")
            email = input("Email: ")
            pwd   = input("Contraseña: ")
            # Ahora register_user levanta ValueError ante datos inválidos
            try:
                register_user(users, name, email, pwd)
                print(Fore.GREEN + "✅ Usuario registrado correctamente.")
            except ValueError as ve:
                print(Fore.RED + f"❌ No se pudo registrar: {ve}")

        elif choice == '2':
            list_users(users)

        elif choice == '3':
            q = input("Nombre a buscar: ")
            found = find_users(users, q)
            if found:
                list_users(found)
            else:
                print(Fore.CYAN + "🔍 No se encontraron coincidencias.")

        elif choice == '4':
            email = input("Email a eliminar: ")
            if delete_user(users, email):
                print(Fore.GREEN + "🗑️ Usuario eliminado.")
            else:
                print(Fore.RED + "❌ No existe ese email.")

        elif choice == '5':
            # Manejamos posibles errores de I/O al guardar
            try:
                save_users(users)
                print(Fore.GREEN + "💾 Cambios guardados. ¡Hasta luego!")
            except Exception as e:
                print(Fore.RED + f"❌ No se pudieron guardar los cambios: {e}")
            break

        else:
            print(Fore.YELLOW + "⚠️ Opción no válida. Elige del 1 al 5.")

    except Exception as e:
        # Para cualquier otro error inesperado
        print(Fore.MAGENTA + f"⚠️ Ocurrió un error inesperado: {e}")

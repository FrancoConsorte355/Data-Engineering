# run_pipeline.py (en la raíz del proyecto)

import os
import time              # Para medir tiempos de ejecución
from dotenv import load_dotenv
load_dotenv()

from src.config import DATA_DIR
from src.ingestion.lector import LectorFactory
from src.processing.sales_manager import SalesManager
from src.db import SessionLocal


def main():
    # 1) Crear sesión real de BD
    session = SessionLocal()
    gestor  = SalesManager(session)

    # 2) Debug: verificar carpeta de trabajo y contenido
    print(f"CWD: {os.getcwd()}")
    print(f"DATA_DIR en uso: {DATA_DIR}")
    print("Carpeta raíz:", os.listdir(os.getcwd()))

    # 3) Asegurar existencia y listar solo archivos regulares
    os.makedirs(DATA_DIR, exist_ok=True)
    all_entries = os.listdir(DATA_DIR)
    nombres = [f for f in all_entries if os.path.isfile(os.path.join(DATA_DIR, f))]
    print("Contenido de DATA_DIR:", nombres)
    if not nombres:
        print(f"ℹ️ No hay archivos en {DATA_DIR}.")
        return

    total_start = time.perf_counter()

    # 4) Procesar cada archivo según su extensión
    for nombre in sorted(nombres):
        ruta = os.path.join(DATA_DIR, nombre)
        ext  = os.path.splitext(nombre)[1].lower()
        # Saltar formatos no soportados
        if ext not in ('.csv', '.json'):
            print(f"⚠️ Saltando '{nombre}', formato no válido: {ext}")
            continue
        try:
            # Strategy: seleccionar lector según extensión
            lector = LectorFactory.get_lector(ext)

            print(f"\n-- Procesando {ruta} con {lector.__class__.__name__} --")
            start = time.perf_counter()

            # 5) Carga de datos a DataFrame genérico
            df = lector.cargar(ruta)
            elapsed = time.perf_counter() - start
            print(f"   ▶️ Lectura en {elapsed:.3f}s >> df.shape = {df.shape}")

            # DEBUG: unas filas iniciales
            print(df.head().to_string(index=False))
            df.info()

            # 6) Procesamiento y persistencia en BD
            t2_start = time.perf_counter()
            gestor.procesar_dataframe(df)
            session.commit()
            t2 = time.perf_counter() - t2_start

            # 7) Archivar archivo
            t3_start = time.perf_counter()
            gestor.marcar_procesado(ruta)
            t3 = time.perf_counter() - t3_start

            print(f"   🗃 Archivado en {t3:.3f}s")
            print(f"⏱ Total archivo: {elapsed + t2 + t3:.3f}s  (proc {t2:.3f}s)")

        except Exception as e:
            session.rollback()
            print(f"❌ Error procesando {nombre}: {e}")

    total_time = time.perf_counter() - total_start
    print(f"\n🎉 Pipeline completada en {total_time:.3f}s")

    # 8) Cerrar sesión
    session.close()


if __name__ == "__main__":
    main()
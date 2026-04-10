"""
enriquecer_escuelas_google.py
=============================
Script para enriquecer dim_escuela_procedencia con direcciones,
coordenadas, municipio y estado usando Google Places API.

Instalación de dependencias:
  pip install psycopg2-binary python-dotenv requests

Uso:
  python enriquecer_escuelas_google.py

Notas:
  - Solo procesa escuelas con direccion = NULL
  - Hace commit cada 10 escuelas por si se interrumpe
  - Las que no encuentra las guarda en 'escuelas_no_encontradas.txt'
    para revisión manual posterior
"""

import os
import time
import requests
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ══════════════════════════════════════════════════════════════════════════════
DB_CONFIG = {
    "host":     os.getenv("DB_HOST", ""),
    "port":     os.getenv("DB_PORT", "5432"),
    "dbname":   os.getenv("DB_NAME", ""),
    "user":     os.getenv("DB_USER", ""),
    "password": os.getenv("DB_PASSWORD", ""),
}

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# Contexto geográfico para mejorar resultados
CONTEXTO = "Yucatán, México"

# Pausa entre requests (segundos)
PAUSA = 0.3


# ══════════════════════════════════════════════════════════════════════════════
# FUNCIÓN DE BÚSQUEDA
# ══════════════════════════════════════════════════════════════════════════════

def buscar_en_google(nombre_escuela):
    """
    Busca una escuela usando Google Places Text Search.
    Intenta primero con nombre completo + contexto,
    luego con palabras clave si no encuentra.
    Retorna un dict con los datos o None si no encuentra.
    """
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_PLACES_KEY no está definida en el .env")

    intentos = [
        f"{nombre_escuela}, {CONTEXTO}",
        f"{nombre_escuela.title()}, {CONTEXTO}",
    ]

    # Intento adicional con palabras clave si el nombre es largo
    palabras = nombre_escuela.split()
    if len(palabras) > 4:
        resumen = " ".join(palabras[:4])
        intentos.append(f"{resumen}, {CONTEXTO}")

    for query in intentos:
        try:
            # ── Text Search para encontrar el lugar ───────────────────────────
            response = requests.get(
                "https://maps.googleapis.com/maps/api/place/textsearch/json",
                params={
                    "query":    query,
                    "key":      GOOGLE_API_KEY,
                    "language": "es",
                    "region":   "mx",
                },
                timeout=10
            )
            response.raise_for_status()
            data = response.json()

            if data.get("status") == "REQUEST_DENIED":
                raise ValueError(f"API key inválida o sin permisos: {data.get('error_message')}")

            resultados = data.get("results", [])
            if not resultados:
                time.sleep(PAUSA)
                continue

            lugar = resultados[0]

            # ── Geocoding para obtener dirección detallada ────────────────────
            lat = lugar["geometry"]["location"]["lat"]
            lng = lugar["geometry"]["location"]["lng"]

            geo_response = requests.get(
                "https://maps.googleapis.com/maps/api/geocode/json",
                params={
                    "latlng":   f"{lat},{lng}",
                    "key":      GOOGLE_API_KEY,
                    "language": "es",
                },
                timeout=10
            )
            geo_response.raise_for_status()
            geo_data = geo_response.json()

            direccion  = lugar.get("formatted_address", "")
            municipio  = ""
            estado     = ""

            # Extrae municipio y estado de los componentes de dirección
            if geo_data.get("results"):
                for componente in geo_data["results"][0].get("address_components", []):
                    tipos = componente.get("types", [])
                    if "locality" in tipos or "sublocality" in tipos:
                        municipio = componente["long_name"]
                    if "administrative_area_level_2" in tipos and not municipio:
                        municipio = componente["long_name"]
                    if "administrative_area_level_1" in tipos:
                        estado = componente["long_name"]
                        estado = estado.replace("Estado de ", "")

            time.sleep(PAUSA)
            return {
                "direccion": direccion,
                "municipio": municipio,
                "estado":    estado,
                "latitud":   lat,
                "longitud":  lng,
            }

        except requests.RequestException as e:
            print(f"    ⚠ Error de red en '{query}': {e}")
            time.sleep(PAUSA)

    return None


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("  Enriquecimiento de escuelas — Google Places API")
    print("=" * 60)

    if not GOOGLE_API_KEY:
        print("\n❌ No se encontró GOOGLE_PLACES_KEY en el archivo .env")
        print("   Agrega tu key y vuelve a ejecutar el script.")
        return

    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = False

    no_encontradas = []

    try:
        cur = conn.cursor()

        # Obtener solo las escuelas que aún no tienen dirección
        cur.execute("""
            SELECT id_escuela, nombre
            FROM datos_reales.dim_escuela_procedencia
            WHERE direccion IS NULL
            ORDER BY id_escuela
        """)
        escuelas = cur.fetchall()
        total = len(escuelas)

        if total == 0:
            print("\n  Todas las escuelas ya tienen dirección. Nada que procesar.")
            return

        print(f"\n  {total} escuelas por enriquecer\n")

        encontradas          = 0
        no_encontradas_count = 0

        for i, (id_escuela, nombre) in enumerate(escuelas, start=1):
            print(f"  [{i}/{total}] {nombre[:60]}...")

            datos = buscar_en_google(nombre)

            if datos:
                cur.execute("""
                    UPDATE datos_reales.dim_escuela_procedencia
                    SET
                        direccion = %s,
                        municipio = %s,
                        estado    = %s,
                        latitud   = %s,
                        longitud  = %s
                    WHERE id_escuela = %s
                """, (
                    datos["direccion"],
                    datos["municipio"],
                    datos["estado"],
                    datos["latitud"],
                    datos["longitud"],
                    id_escuela
                ))
                encontradas += 1
                print(f"    ✓ {datos['municipio']}, {datos['estado']}")
            else:
                no_encontradas.append(f"{id_escuela}\t{nombre}")
                no_encontradas_count += 1
                print(f"    ✗ No encontrada")

            # Commit cada 10 escuelas para no perder progreso
            if i % 10 == 0:
                conn.commit()
                print(f"\n  --- Guardado parcial ({i}/{total}) ---\n")

        # Commit final
        conn.commit()

        # Guardar no encontradas para revisión manual
        if no_encontradas:
            with open("escuelas_no_encontradas.txt", "w", encoding="utf-8") as f:
                f.write("id_escuela\tnombre\n")
                f.write("\n".join(no_encontradas))
            print(f"\n  Escuelas no encontradas guardadas en: escuelas_no_encontradas.txt")
            print(f"  Puedes actualizarlas manualmente con:")
            print(f"  UPDATE datos_reales.dim_escuela_procedencia")
            print(f"  SET direccion='...', municipio='...', estado='Yucatán',")
            print(f"      latitud=20.96, longitud=-89.59")
            print(f"  WHERE id_escuela = <id>;")

        print("\n" + "=" * 60)
        print(f"  ✅ Proceso completado")
        print(f"     Encontradas    : {encontradas}")
        print(f"     No encontradas : {no_encontradas_count}")
        print("=" * 60)

    except Exception as e:
        conn.rollback()
        print(f"\n❌ Error — se hizo rollback")
        print(f"   Detalle: {e}")
        raise
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    main()
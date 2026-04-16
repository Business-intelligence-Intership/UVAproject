"""
insertar_sinteticos.py
======================
Script para insertar datos sintéticos desde archivos CSV
en PostgreSQL (schema: datos_reales).

Archivos esperados (en la misma carpeta que este script):
  alumnos_2018.csv, alumnos_2019.csv, ... alumnos_2023.csv

Instalación de dependencias:
  pip install psycopg2-binary python-dotenv pandas

Uso:
  python insertar_sinteticos.py
"""

import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv()

# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ══════════════════════════════════════════════════════════════════════════════
DB_CONFIG = {
    "host":     os.getenv("DB_HOST", "localhost"),
    "port":     os.getenv("DB_PORT", "5432"),
    "dbname":   os.getenv("DB_NAME", ""),
    "user":     os.getenv("DB_USER", ""),
    "password": os.getenv("DB_PASSWORD", ""),
}

# Archivos CSV a procesar en orden cronológico
ARCHIVOS_CSV = [
    "alumnos_2018.csv",
    "alumnos_2019.csv",
    "alumnos_2020.csv",
    "alumnos_2021.csv",
    "alumnos_2022.csv",
    "alumnos_2023.csv",
]

# ══════════════════════════════════════════════════════════════════════════════
# MAPEOS DE NORMALIZACIÓN
# Convierte los valores del CSV al estándar de tus tablas
# ══════════════════════════════════════════════════════════════════════════════
MAPA_SEXO = {
    "hombre":    "Masculino",
    "mujer":     "Femenino",
    "masculino": "Masculino",
    "femenino":  "Femenino",
}

MAPA_MODALIDAD = {
    "escolar":       "Escolarizada",
    "mixto":         "Mixto/Sabatino",
    "escolarizada":  "Escolarizada",
    "mixto/sabatino":"Mixto/Sabatino",
}

# "2023-1" → "Enero-Abril", "2023-2" → "Mayo-Agosto", "2023-3" → "Septiembre-Diciembre"
MAPA_CICLO = {
    "1": "Enero-Abril",
    "2": "Mayo-Agosto",
    "3": "Septiembre-Diciembre",
}

TIPO_CICLO_CARRERA = {
    "Ingeniería Civil":                      "Cuatrimestral",
    "Ingeniería De Procesos De Manufactura": "Cuatrimestral",
    "Administración de Empresas":            "Cuatrimestral",
    "Arquitectura":                          "Cuatrimestral",
    "Contaduría Pública":                    "Cuatrimestral",
    "Criminología":                          "Cuatrimestral",
    "Derecho":                               "Cuatrimestral",
    "Diseño de Modas":                       "Cuatrimestral",
    "Ciencias De La Educación":              "Cuatrimestral",
    "Enfermería":                            "Cuatrimestral",
    "Fisioterapia":                          "Cuatrimestral",
    "Gastronomía":                           "Cuatrimestral",
    "Nutrición":                             "Cuatrimestral",
    "Psicología":                            "Cuatrimestral",
    "Odontología":                           "Semestral",
}

# ══════════════════════════════════════════════════════════════════════════════
# FUNCIONES DE NORMALIZACIÓN
# ══════════════════════════════════════════════════════════════════════════════

def normalizar_sexo(valor):
    """Convierte Hombre/Mujer al estándar Masculino/Femenino."""
    if pd.isna(valor):
        return None
    limpio = str(valor).strip().lower()
    resultado = MAPA_SEXO.get(limpio)
    if not resultado:
        print(f"Sexo no reconocido: '{valor}' — se omite")
    return resultado


def normalizar_modalidad(valor):
    """Convierte Escolar/Mixto al estándar Escolarizada/Mixto/Sabatino."""
    if pd.isna(valor):
        return None
    limpio = str(valor).strip().lower()
    resultado = MAPA_MODALIDAD.get(limpio)
    if not resultado:
        print(f"Modalidad no reconocida: '{valor}' — se omite")
    return resultado


def normalizar_ciclo(valor):
    """
    Convierte '2023-1' → ('Enero-Abril', 2023)
    Retorna (nombre_ciclo, año) o (None, None) si no se reconoce.
    """
    if pd.isna(valor):
        return None, None
    partes = str(valor).strip().split("-")
    if len(partes) != 2:
        print(f"Ciclo con formato inesperado: '{valor}'")
        return None, None
    año_str, num_ciclo = partes
    nombre_ciclo = MAPA_CICLO.get(num_ciclo)
    if not nombre_ciclo:
        print(f"Número de ciclo no reconocido: '{num_ciclo}' en '{valor}'")
        return None, None
    return nombre_ciclo, int(año_str)


# ══════════════════════════════════════════════════════════════════════════════
# FUNCIONES DE INSERCIÓN
# ══════════════════════════════════════════════════════════════════════════════

def obtener_o_crear_carrera(cur, nombre, modalidad, turno, año):
    """
    Busca la carrera por nombre+modalidad. Si existe la actualiza con turno,
    si no existe la crea. Retorna id_carrera.
    """
    tipo_ciclo = TIPO_CICLO_CARRERA.get(nombre, "Cuatrimestral")
    cur.execute("""
        INSERT INTO datos_reales.dim_carrera
            (nombre, clave_carrera, modalidad, tipo_ciclo, ciclos_periodo, año_inicio, turno)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (nombre, modalidad) DO UPDATE
            SET turno = EXCLUDED.turno
        RETURNING id_carrera
    """, (
        nombre,
        "00",       # clave provisional para sintéticos sin clave oficial
        modalidad,
        tipo_ciclo,
        ["Enero-Abril", "Mayo-Agosto", "Septiembre-Diciembre"],
        año,
        turno
    ))
    return cur.fetchone()[0]


def obtener_o_crear_escuela(cur, nombre, ubicacion):
    """
    Busca la escuela por nombre. Si existe actualiza ubicacion,
    si no existe la crea. Retorna id_escuela.
    """
    cur.execute("""
        INSERT INTO datos_reales.dim_escuela_procedencia
            (nombre, ubicacion, es_odontologia)
        VALUES (%s, %s, FALSE)
        ON CONFLICT (nombre) DO UPDATE
            SET ubicacion = COALESCE(EXCLUDED.ubicacion, dim_escuela_procedencia.ubicacion)
        RETURNING id_escuela
    """, (nombre, ubicacion))
    return cur.fetchone()[0]


def obtener_o_crear_periodo(cur, nombre_ciclo, año, tipo_ciclo):
    """
    Busca el periodo por año+ciclo+tipo. Si no existe lo crea.
    Retorna id_periodo.
    """
    fechas = {
        ("Enero-Abril",          "Cuatrimestral"): ("01-01", "04-30"),
        ("Mayo-Agosto",          "Cuatrimestral"): ("05-01", "08-31"),
        ("Septiembre-Diciembre", "Cuatrimestral"): ("09-01", "12-31"),
        ("Enero-Junio",          "Semestral"):     ("01-01", "06-30"),
        ("Agosto-Diciembre",     "Semestral"):     ("08-01", "12-31"),
    }
    numeros = {
        "Enero-Abril": 1, "Mayo-Agosto": 2, "Septiembre-Diciembre": 3,
        "Enero-Junio": 1, "Agosto-Diciembre": 2,
    }
    fi, ff = fechas.get((nombre_ciclo, tipo_ciclo), ("01-01", "12-31"))
    num    = numeros.get(nombre_ciclo, 1)

    cur.execute("""
        INSERT INTO datos_reales.dim_periodo
            (año, nombre_ciclo, numero_ciclo, tipo_ciclo, fecha_inicio, fecha_fin)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (año, nombre_ciclo, tipo_ciclo) DO NOTHING
        RETURNING id_periodo
    """, (año, nombre_ciclo, num, tipo_ciclo, f"{año}-{fi}", f"{año}-{ff}"))

    row = cur.fetchone()
    if row:
        return row[0]

    cur.execute("""
        SELECT id_periodo FROM datos_reales.dim_periodo
        WHERE año = %s AND nombre_ciclo = %s AND tipo_ciclo = %s
    """, (año, nombre_ciclo, tipo_ciclo))
    return cur.fetchone()[0]


def insertar_alumno(cur, matricula, fecha_nac, nacionalidad, lugar, colonia, año):
    """Inserta el alumno y retorna su id. Si ya existe, lo omite y retorna el existente."""
    cur.execute("""
        INSERT INTO datos_reales.dim_alumno
            (matricula, fecha_nacimiento, nacionalidad, lugar_nacimiento, colonia, año_ingreso)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (matricula) DO NOTHING
        RETURNING id_alumno
    """, (matricula, fecha_nac, nacionalidad, lugar, colonia, año))

    row = cur.fetchone()
    if row:
        return row[0]

    cur.execute(
        "SELECT id_alumno FROM datos_reales.dim_alumno WHERE matricula = %s",
        (matricula,)
    )
    return cur.fetchone()[0]


# ══════════════════════════════════════════════════════════════════════════════
# PROCESADOR DE CSV
# ══════════════════════════════════════════════════════════════════════════════

def procesar_csv(cur, ruta_csv):
    """Lee un CSV y procesa cada fila insertando en el orden correcto."""
    print(f"\n  Leyendo {ruta_csv}...")
    df = pd.read_csv(ruta_csv, parse_dates=["fecha_nacimiento"])
    print(f"  {len(df)} filas encontradas")

    filas_fact   = []
    omitidas     = 0
    procesadas   = 0

    # Cachés para evitar queries repetidas a BD por cada fila
    cache_carreras = {}
    cache_escuelas = {}
    cache_periodos = {}

    for _, row in df.iterrows():

        # ── Normalizar valores ────────────────────────────────────────────────
        sexo      = normalizar_sexo(row["sexo"])
        modalidad = normalizar_modalidad(row["modalidad"])
        nombre_ciclo, año = normalizar_ciclo(row["ciclo"])

        if not all([sexo, modalidad, nombre_ciclo, año]):
            omitidas += 1
            continue

        carrera_nombre = str(row["carrera"]).strip()
        turno          = str(row["turno"]).strip()
        escuela_nombre = str(row["escuela_procedencia"]).strip()
        ubicacion      = str(row["ubicacion_escuela_procedencia"]).strip()
        matricula      = str(row["matricula"]).strip()
        nacionalidad   = str(row["nacionalidad"]).strip()
        lugar          = str(row["lugar_nacimiento"]).strip()
        colonia        = str(row["colonia"]).strip()
        fecha_nac      = row["fecha_nacimiento"].date() if pd.notna(row["fecha_nacimiento"]) else None
        tipo_ciclo     = TIPO_CICLO_CARRERA.get(carrera_nombre, "Cuatrimestral")

        # ── dim_carrera (con caché) ───────────────────────────────────────────
        clave_carrera = (carrera_nombre, modalidad)
        if clave_carrera not in cache_carreras:
            cache_carreras[clave_carrera] = obtener_o_crear_carrera(
                cur, carrera_nombre, modalidad, turno, año
            )
        id_carrera = cache_carreras[clave_carrera]

        # ── dim_escuela_procedencia (con caché) ───────────────────────────────
        if escuela_nombre not in cache_escuelas:
            cache_escuelas[escuela_nombre] = obtener_o_crear_escuela(
                cur, escuela_nombre, ubicacion
            )
        id_escuela = cache_escuelas[escuela_nombre]

        # ── dim_periodo (con caché) ───────────────────────────────────────────
        clave_periodo = (año, nombre_ciclo, tipo_ciclo)
        if clave_periodo not in cache_periodos:
            cache_periodos[clave_periodo] = obtener_o_crear_periodo(
                cur, nombre_ciclo, año, tipo_ciclo
            )
        id_periodo = cache_periodos[clave_periodo]

        # ── dim_alumno ────────────────────────────────────────────────────────
        id_alumno = insertar_alumno(
            cur, matricula, fecha_nac, nacionalidad, lugar, colonia, año
        )

        # ── Acumular fila para fact_matricula ─────────────────────────────────
        # Calculamos edad desde fecha_nacimiento
        if fecha_nac:
            from datetime import date
            hoy = date.today()
            edad = hoy.year - fecha_nac.year - (
                (hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day)
            )
        else:
            edad = None

        filas_fact.append((
            id_carrera,
            id_periodo,
            id_escuela,
            edad,
            sexo,
            1,          # cantidad_alumnos = 1 (registros individuales)
            False,      # es_dato_real = False (son sintéticos)
            id_alumno
        ))
        procesadas += 1

    # ── Insertar fact_matricula en bloque ─────────────────────────────────────
    if filas_fact:
        execute_values(cur, """
            INSERT INTO datos_reales.fact_matricula
                (id_carrera, id_periodo, id_escuela, edad, sexo,
                 cantidad_alumnos, es_dato_real, id_alumno)
            VALUES %s
        """, filas_fact)

    print(f"  ✓ {procesadas} filas insertadas  |  ⚠ {omitidas} omitidas")
    return procesadas, omitidas


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("  Inserción de datos sintéticos — Universidad")
    print("=" * 60)

    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = False

    total_procesadas = 0
    total_omitidas   = 0

    try:
        cur = conn.cursor()

        for archivo in ARCHIVOS_CSV:
            if not os.path.exists(archivo):
                print(f"\n  ⚠ Archivo no encontrado, se omite: {archivo}")
                continue

            p, o = procesar_csv(cur, archivo)
            total_procesadas += p
            total_omitidas   += o

        conn.commit()
        print("\n" + "=" * 60)
        print(f"  ✅ Inserción completada")
        print(f"     Total insertados : {total_procesadas}")
        print(f"     Total omitidos   : {total_omitidas}")
        print("=" * 60)

    except Exception as e:
        conn.rollback()
        print(f"\n❌ Error — se hizo rollback de toda la transacción")
        print(f"   Detalle: {e}")
        raise
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    main()

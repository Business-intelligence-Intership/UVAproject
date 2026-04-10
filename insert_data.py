"""
insertar_datos.py
=================
Script para insertar los datos reales de matrícula universitaria
en PostgreSQL (schema: datos_reales).

Estructura esperada de tus archivos:
  - datos_2024.py  → diccionarios del año 2024
  - datos_2025.py  → diccionarios del año 2025

Instalación de dependencias:
  pip install psycopg2-binary python-dotenv

Uso:
  1. Crea un archivo .env con tus credenciales (ver abajo)
  2. Asegúrate de que el schema y las tablas ya existen (SQL previo)
  3. Ejecuta: python insertar_datos.py
"""

import psycopg2
from psycopg2.extras import execute_values
import os
from dotenv import load_dotenv

# ── Importa tus archivos de datos ──────────────────────────────────────────────
# Ajusta los nombres de módulo si tus archivos se llaman distinto
import datos_2024 as d24
import datos_2025 as d25


# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN — Carga credenciales desde .env
# ══════════════════════════════════════════════════════════════════════════════
load_dotenv()

DB_CONFIG = {
    "host":     os.getenv("DB_HOST", "localhost"),
    "port":     os.getenv("DB_PORT", "5432"),
    "dbname":   os.getenv("DB_NAME", ""),
    "user":     os.getenv("DB_USER", ""),
    "password": os.getenv("DB_PASSWORD", ""),
}


# ══════════════════════════════════════════════════════════════════════════════
# DATOS DE REFERENCIA
# (Cópialos tal como los tienes en tu código, aquí van los catálogos fijos)
# ══════════════════════════════════════════════════════════════════════════════

TIPO_CICLO = {
    "Ingeniería Civil":                    "Cuatrimestral",
    "Ingeniería De Procesos De Manufactura": "Cuatrimestral",
    "Administración de Empresas":          "Cuatrimestral",
    "Arquitectura":                        "Cuatrimestral",
    "Contaduría Pública":                  "Cuatrimestral",
    "Criminología":                        "Cuatrimestral",
    "Derecho":                             "Cuatrimestral",
    "Diseño de Modas":                     "Cuatrimestral",
    "Ciencias De La Educación":            "Cuatrimestral",
    "Enfermería":                          "Cuatrimestral",
    "Fisioterapia":                        "Cuatrimestral",
    "Gastronomía":                         "Cuatrimestral",
    "Nutrición":                           "Cuatrimestral",
    "Psicología":                          "Cuatrimestral",
    "Odontología":                         "Semestral",
}

CICLOS = {
    "Cuatrimestral": ["Enero-Abril", "Mayo-Agosto", "Septiembre-Diciembre"],
    "Semestral":     ["Enero-Junio", "Agosto-Diciembre"],
}

# Claves por carrera y modalidad
# Agrega aquí TODAS tus claves tal como las tienes en CLAVES_CARRERA
CLAVES_CARRERA = {
    "Arquitectura":                          {"Escolarizada": "01", "Mixto/Sabatino": "20"},
    "Administración de Empresas":            {"Escolarizada": "14", "Mixto/Sabatino": "27"},
    "Contaduría Pública":                    {"Escolarizada": "12", "Mixto/Sabatino": "32"},
    "Criminología":                          {"Escolarizada": "16"},
    "Derecho":                               {"Escolarizada": "08", "Mixto/Sabatino": "35"},
    "Diseño de Modas":                       {"Escolarizada": "06", "Mixto/Sabatino": "33"},
    "Ciencias De La Educación":              {"Escolarizada": "02", "Mixto/Sabatino": "31"},
    "Enfermería":                            {"Escolarizada": "09"},
    "Fisioterapia":                          {"Escolarizada": "10"},
    "Gastronomía":                           {"Escolarizada": "04", "Mixto/Sabatino": "36"},
    "Nutrición":                             {"Escolarizada": "13", "Mixto/Sabatino": "25"},
    "Odontología":                           {"Escolarizada": "17"},
    "Psicología":                            {"Escolarizada": "15", "Mixto/Sabatino": "28"},
    "Ingeniería Civil":                      {"Mixto/Sabatino": "37"},
    "Ingeniería De Procesos De Manufactura": {"Mixto/Sabatino": "38"},
}

# ──────────────────────────────────────────────────────────────────────────────
# CATÁLOGO DE CARRERAS POR AÑO
# Cada entrada: (nombre_carrera, modalidad, año_inicio)
# ──────────────────────────────────────────────────────────────────────────────
CARRERAS_2024 = [
    ("Administración de Empresas",  "Mixto/Sabatino", 2024),
    ("Administración de Empresas",  "Escolarizada",   2024),
    ("Arquitectura",                "Mixto/Sabatino", 2024),
    ("Arquitectura",                "Escolarizada",   2024),
    ("Contaduría Pública",          "Mixto/Sabatino", 2024),
    ("Contaduría Pública",          "Escolarizada",   2024),
    ("Criminología",                "Escolarizada",   2024),
    ("Derecho",                     "Mixto/Sabatino", 2024),
    ("Derecho",                     "Escolarizada",   2024),
    ("Diseño de Modas",             "Mixto/Sabatino", 2024),
    ("Diseño de Modas",             "Escolarizada",   2024),
    ("Ciencias De La Educación",    "Mixto/Sabatino", 2024),
    ("Ciencias De La Educación",    "Escolarizada",   2024),
    ("Enfermería",                  "Escolarizada",   2024),
    ("Fisioterapia",                "Escolarizada",   2024),
    ("Gastronomía",                 "Mixto/Sabatino", 2024),
    ("Gastronomía",                 "Escolarizada",   2024),
    ("Nutrición",                   "Mixto/Sabatino", 2024),
    ("Nutrición",                   "Escolarizada",   2024),
    ("Odontología",                 "Escolarizada",   2024),
    ("Psicología",                  "Mixto/Sabatino", 2024),
    ("Psicología",                  "Escolarizada",   2024),
    ("Ingeniería Civil",            "Mixto/Sabatino", 2024),
]

CARRERAS_2025 = CARRERAS_2024 + [
    ("Ingeniería De Procesos De Manufactura", "Mixto/Sabatino", 2025),
]

# ──────────────────────────────────────────────────────────────────────────────
# DATOS DE MATRÍCULA (edades + sexo)
# Formato esperado de cada diccionario en datos_2024.py / datos_2025.py:
#   { edad_int: {"Masculino": n, "Femenino": n}, ... }
#
# La clave del mapa es: (nombre_carrera, modalidad, año)
# Ajusta los nombres de variables según como las tienes en tus archivos
# ──────────────────────────────────────────────────────────────────────────────
MATRICULA = {
    # ── 2024 ────────────────────────────────────────────────────────────────
    ("Administración de Empresas", "Mixto/Sabatino", 2024): d24.edades_administracion_mix_2024,
    ("Administración de Empresas", "Escolarizada",   2024): d24.edades_administracion_escolarizada_2024,
    ("Arquitectura",               "Mixto/Sabatino", 2024): d24.edades_arquitectura_mix_2024,
    ("Arquitectura",               "Escolarizada",   2024): d24.edades_arquitectura_escolarizada_2024,
    ("Contaduría Pública",         "Mixto/Sabatino", 2024): d24.edades_contaduria_mix_2024,
    ("Contaduría Pública",         "Escolarizada",   2024): d24.edades_contaduria_escolarizada_2024,
    ("Criminología",               "Escolarizada",   2024): d24.edades_criminologia_escolarizada_2024,
    ("Derecho",                    "Mixto/Sabatino", 2024): d24.edades_derecho_mix_2024,
    ("Derecho",                    "Escolarizada",   2024): d24.edades_derecho_escolarizada_2024,
    ("Diseño de Modas",            "Mixto/Sabatino", 2024): d24.edades_diseno_modas_mix_2024,
    ("Diseño de Modas",            "Escolarizada",   2024): d24.edades_diseno_modas_escolarizada_2024,
    ("Ciencias De La Educación",   "Mixto/Sabatino", 2024): d24.edades_educacion_mix_2024,
    ("Enfermería",                 "Escolarizada",   2024): d24.edades_enfermeria_escolarizada_2024,
    ("Fisioterapia",               "Escolarizada",   2024): d24.edades_fisioterapia_escolarizada_2024,
    ("Gastronomía",                "Mixto/Sabatino", 2024): d24.edades_gastronomia_mix_2024,
    ("Gastronomía",                "Escolarizada",   2024): d24.edades_gastronomia_escolarizada_2024,
    ("Nutrición",                  "Mixto/Sabatino", 2024): d24.edades_nutricion_mix_2024,
    ("Nutrición",                  "Escolarizada",   2024): d24.edades_nutricion_escolarizada_2024,
    ("Odontología",                "Escolarizada",   2024): d24.edades_odontologia_escolarizada_2024,
    ("Psicología",                 "Mixto/Sabatino", 2024): d24.edades_psicologia_mix_2024,
    ("Psicología",                 "Escolarizada",   2024): d24.edades_psicologia_escolarizada_2024,
    ("Ingeniería Civil",           "Mixto/Sabatino", 2024): d24.edades_ingenieria_civil_mix_2024,

   

    # ── 2025 ────────────────────────────────────────────────────────────────
    ("Administración de Empresas", "Mixto/Sabatino", 2025): d25.edades_administracion_empresas_mix_2025,
    ("Administración de Empresas", "Escolarizada",   2025): d25.edades_administracion_empresas_escolarizada_2025,
    ("Arquitectura",               "Mixto/Sabatino", 2025): d25.edades_arquitectura_mix_2025,
    ("Arquitectura",               "Escolarizada",   2025): d25.edades_arquitectura_escolarizada_2025,
    ("Contaduría Pública",         "Mixto/Sabatino", 2025): d25.edades_contaduria_mix_2025,
    ("Contaduría Pública",         "Escolarizada",   2025): d25.edades_contaduria_escolarizada_2025,
    ("Criminología",               "Escolarizada",   2025): d25.edades_criminologia_escolarizada_2025,
    ("Derecho",                    "Mixto/Sabatino", 2025): d25.edades_derecho_mix_2025,
    ("Derecho",                    "Escolarizada",   2025): d25.edades_derecho_escolarizada_2025,
    ("Diseño de Modas",            "Mixto/Sabatino", 2025): d25.edades_diseno_modas_mix_2025,
    ("Diseño de Modas",            "Escolarizada",   2025): d25.edades_diseno_modas_escolarizada_2025,
    ("Ciencias De La Educación",   "Mixto/Sabatino", 2025): d25.edades_educacion_mix_2025,
    ("Enfermería",                 "Escolarizada",   2025): d25.edades_enfermeria_escolarizada_2025,
    ("Fisioterapia",               "Escolarizada",   2025): d25.edades_fisioterapia_escolarizada_2025,
    ("Gastronomía",                "Mixto/Sabatino", 2025): d25.edades_gastronomia_mix_2025,
    ("Gastronomía",                "Escolarizada",   2025): d25.edades_gastronomia_escolarizada_2025,
    ("Nutrición",                  "Mixto/Sabatino", 2025): d25.edades_nutricion_mix_2025,
    ("Nutrición",                  "Escolarizada",   2025): d25.edades_nutricion_escolarizada_2025,
    ("Odontología",                "Escolarizada",   2025): d25.edades_odontologia_escolarizada_2025,
    ("Psicología",                 "Mixto/Sabatino", 2025): d25.edades_psicologia_mix_2025,
    ("Psicología",                 "Escolarizada",   2025): d25.edades_psicologia_escolarizada_2025,
    ("Ingeniería Civil",           "Mixto/Sabatino", 2025): d25.edades_ingenieria_civil_mix_2025,
    ("Ingeniería De Procesos De Manufactura", "Mixto/Sabatino", 2025): d25.edades_procesos_manufactura_mix_2025,
    
}

# ──────────────────────────────────────────────────────────────────────────────
# ESCUELAS DE PROCEDENCIA GENERALES (todas las carreras excepto odontología)
# Formato esperado: { "NOMBRE ESCUELA": num_alumnos, ... }
# ──────────────────────────────────────────────────────────────────────────────
ESCUELAS_GENERALES = {
    2024: d24.escuelas_procedencia_general_2024,   
    2025: d25.escuelas_procedencia_general_2025,
}

# Escuelas de procedencia exclusivas de Odontología
ESCUELAS_ODONTOLOGIA = {
    2024: d24.escuelas_procedencia_odontologia_2024,
    2025: d25.escuelas_procedencia_odontologia_2025,
}


# ══════════════════════════════════════════════════════════════════════════════
# FUNCIONES DE INSERCIÓN
# ══════════════════════════════════════════════════════════════════════════════

def insertar_carreras(cur, carreras: list) -> dict:
    """
    Inserta las carreras en dim_carrera.
    Retorna un dict {(nombre, modalidad): id_carrera}
    """
    print("\n[1/4] Insertando carreras...")
    mapa = {}

    for nombre, modalidad, año_inicio in carreras:
        tipo  = TIPO_CICLO[nombre]
        ciclos = CICLOS[tipo]
        clave  = CLAVES_CARRERA.get(nombre, {}).get(modalidad, "??")

        cur.execute("""
            INSERT INTO datos_reales.dim_carrera
                (nombre, clave_carrera, modalidad, tipo_ciclo, ciclos_periodo, año_inicio)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (nombre, modalidad) DO UPDATE
                SET clave_carrera  = EXCLUDED.clave_carrera,
                    tipo_ciclo     = EXCLUDED.tipo_ciclo,
                    ciclos_periodo = EXCLUDED.ciclos_periodo,
                    año_inicio     = EXCLUDED.año_inicio
            RETURNING id_carrera
        """, (nombre, clave, modalidad, tipo, ciclos, año_inicio))

        id_carrera = cur.fetchone()[0]
        mapa[(nombre, modalidad)] = id_carrera
        print(f"  ✓ {nombre} [{modalidad}] → id={id_carrera}")

    return mapa


def insertar_periodos(cur, años: list) -> dict:
    """
    Inserta los periodos (ciclos) en dim_periodo para cada año dado.
    Retorna un dict {(año, nombre_ciclo, tipo_ciclo): id_periodo}
    """
    print("\n[2/4] Insertando periodos...")
    mapa = {}

    fechas = {
        # Cuatrimestrales
        ("Enero-Abril",          "Cuatrimestral"): ("01-01", "04-30"),
        ("Mayo-Agosto",          "Cuatrimestral"): ("05-01", "08-31"),
        ("Septiembre-Diciembre", "Cuatrimestral"): ("09-01", "12-31"),
        # Semestrales
        ("Enero-Junio",          "Semestral"):     ("01-01", "06-30"),
        ("Agosto-Diciembre",     "Semestral"):     ("08-01", "12-31"),
    }

    for año in años:
        for tipo, ciclos_lista in CICLOS.items():
            for num, nombre_ciclo in enumerate(ciclos_lista, start=1):
                fi, ff = fechas[(nombre_ciclo, tipo)]
                cur.execute("""
                    INSERT INTO datos_reales.dim_periodo
                        (año, nombre_ciclo, numero_ciclo, tipo_ciclo, fecha_inicio, fecha_fin)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (año, nombre_ciclo, tipo_ciclo) DO NOTHING
                    RETURNING id_periodo
                """, (año, nombre_ciclo, num, tipo, f"{año}-{fi}", f"{año}-{ff}"))

                row = cur.fetchone()
                if row:
                    id_periodo = row[0]
                else:
                    cur.execute("""
                        SELECT id_periodo FROM datos_reales.dim_periodo
                        WHERE año=%s AND nombre_ciclo=%s AND tipo_ciclo=%s
                    """, (año, nombre_ciclo, tipo))
                    id_periodo = cur.fetchone()[0]

                mapa[(año, nombre_ciclo, tipo)] = id_periodo
                print(f"  ✓ {año} | {nombre_ciclo} [{tipo}] → id={id_periodo}")

    return mapa


def insertar_escuelas(cur, escuelas_dict: dict, es_odontologia: bool) -> dict:
    """
    Inserta escuelas en dim_escuela_procedencia.
    Retorna un dict {nombre_escuela: id_escuela}
    """
    mapa = {}
    for nombre in escuelas_dict.keys():
        cur.execute("""
            INSERT INTO datos_reales.dim_escuela_procedencia
                (nombre, es_odontologia)
            VALUES (%s, %s)
            ON CONFLICT (nombre) DO UPDATE
                SET es_odontologia = EXCLUDED.es_odontologia
            RETURNING id_escuela
        """, (nombre, es_odontologia))
        mapa[nombre] = cur.fetchone()[0]
    return mapa


def insertar_matricula(cur, mapa_carreras: dict, mapa_periodos: dict):
    """
    Inserta los registros de matrícula en fact_matricula.
    Usa el primer periodo del año como periodo de referencia del reporte.
    """
    print("\n[4/4] Insertando matrícula (edades/sexo)...")
    filas = []

    for (nombre, modalidad, año), datos_edad in MATRICULA.items():
        id_carrera = mapa_carreras.get((nombre, modalidad))
        if not id_carrera:
            print(f"  ⚠ Carrera no encontrada: {nombre} [{modalidad}]")
            continue

        tipo = TIPO_CICLO[nombre]
        # Usamos el primer ciclo del año como periodo de referencia del reporte
        primer_ciclo = CICLOS[tipo][0]
        id_periodo = mapa_periodos.get((año, primer_ciclo, tipo))
        if not id_periodo:
            print(f"  ⚠ Periodo no encontrado: {año} {primer_ciclo} [{tipo}]")
            continue

        for edad, sexos in datos_edad.items():
            for sexo, cantidad in sexos.items():
                sexo_limpio = sexo.strip().capitalize()
                if sexo_limpio not in ("Masculino", "Femenino"):
                    print(f" Sexo desconocido: '{sexo}' - Se omite")
                    continue
                if cantidad > 0:
                    filas.append((
                        id_carrera,
                        id_periodo,
                        None,       # id_escuela: NULL (edad/sexo no viene enlazado a escuela)
                        int(edad),
                        sexo,
                        cantidad,
                        True        # es_dato_real
                    ))

    execute_values(cur, """
        INSERT INTO datos_reales.fact_matricula
            (id_carrera, id_periodo, id_escuela, edad, sexo, cantidad_alumnos, es_dato_real)
        VALUES %s
    """, filas)

    print(f"  ✓ {len(filas)} registros insertados en fact_matricula")


def insertar_matricula_escuelas(cur, mapa_carreras: dict, mapa_periodos: dict,
                                 mapa_escuelas: dict, año: int, es_odonto: bool):
    """
    Inserta en fact_matricula los registros de escuelas de procedencia.
    Como no tienes la carrera específica de cada escuela general,
    se registran con id_carrera = NULL usando una fila especial de agregado.
    Para odontología sí se enlaza la carrera.
    """
    print(f"\n  Insertando escuelas de procedencia {'(Odontología)' if es_odonto else '(Generales)'} {año}...")
    filas = []
    tipo_ref = "Semestral" if es_odonto else "Cuatrimestral"
    primer_ciclo = CICLOS[tipo_ref][0]
    id_periodo = mapa_periodos.get((año, primer_ciclo, tipo_ref))

    id_carrera_odonto = None
    if es_odonto:
        id_carrera_odonto = mapa_carreras.get(("Odontología", "Escolarizada"))

    diccionario = ESCUELAS_ODONTOLOGIA[año] if es_odonto else ESCUELAS_GENERALES[año]

    for nombre_escuela, cantidad in diccionario.items():
        id_escuela = mapa_escuelas.get(nombre_escuela)
        if not id_escuela:
            print(f"    ⚠ Escuela no encontrada en mapa: {nombre_escuela}")
            continue
        filas.append((
            id_carrera_odonto,  # NULL para generales, id real para odonto
            id_periodo,
            id_escuela,
            None,               # edad: no disponible en este agregado
            None,               # sexo: no disponible en este agregado
            cantidad,
            True
        ))

    # Para escuelas necesitamos INSERT sin las restricciones NOT NULL de edad/sexo
    # Por eso la fact_matricula debe permitir NULL en edad y sexo para este caso
    # (ajusta el CREATE TABLE si pusiste NOT NULL en esos campos)
    if filas:
        execute_values(cur, """
            INSERT INTO datos_reales.fact_matricula
                (id_carrera, id_periodo, id_escuela, edad, sexo, cantidad_alumnos, es_dato_real)
            VALUES %s
        """, filas)
        print(f"    ✓ {len(filas)} escuelas insertadas")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("  Inserción de datos reales — Universidad")
    print("=" * 60)

    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = False  # Usamos transacción única: todo o nada

    try:
        cur = conn.cursor()

        # 1. Carreras (unión de ambos años sin duplicar)
        todas_carreras = list({(n, m, a) for n, m, _ in CARRERAS_2024
                                for a in [2024]} |
                              {(n, m, 2025) for n, m, _ in CARRERAS_2025})
        # Simplificado: inserta con año_inicio correcto
        mapa_carreras = insertar_carreras(cur, CARRERAS_2024 + [
            c for c in CARRERAS_2025 if c not in CARRERAS_2024
        ])

        # 2. Periodos para 2024 y 2025
        mapa_periodos = insertar_periodos(cur, [2024, 2025])

        # 3. Escuelas de procedencia
        print("\n[3/4] Insertando escuelas de procedencia...")
        mapa_escuelas = {}
        for año in [2024, 2025]:
            mapa_escuelas.update(
                insertar_escuelas(cur, ESCUELAS_GENERALES[año],   es_odontologia=False)
            )
            mapa_escuelas.update(
                insertar_escuelas(cur, ESCUELAS_ODONTOLOGIA[año], es_odontologia=True)
            )
        print(f"  ✓ {len(mapa_escuelas)} escuelas registradas en total")

        # 4. Matrícula por edad/sexo
        insertar_matricula(cur, mapa_carreras, mapa_periodos)

        # 5. Matrícula por escuelas de procedencia
        for año in [2024, 2025]:
            insertar_matricula_escuelas(
                cur, mapa_carreras, mapa_periodos,
                mapa_escuelas, año, es_odonto=False
            )
            insertar_matricula_escuelas(
                cur, mapa_carreras, mapa_periodos,
                mapa_escuelas, año, es_odonto=True
            )

        conn.commit()
        print("\n" + "=" * 60)
        print("  ✅ Todos los datos insertados correctamente")
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
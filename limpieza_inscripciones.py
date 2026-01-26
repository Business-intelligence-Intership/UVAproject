import pandas as pd
import glob
import os

# =========================
# CONFIG
# =========================
INPUT_DIR = "csv_vizcaya"
OUTPUT_DIR = "csv_vizcaya_limpios"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================
# DICCIONARIOS DE LIMPIEZA
# =========================
MAP_SEXO = {
    "M": "M",
    "H": "M",
    "Masculino": "M",
    "F": "F",
    "Fem": "F",
    "Femenino": "F"
}

MAP_NACIONALIDAD = {
    "Mexicana": "Mexicana",
    "mexicano": "Mexicana",
    "MX": "Mexicana",
    "México": "Mexicana"
}

MAP_NIVEL = {
    "LIC": "Licenciatura",
    "Licenciatura": "Licenciatura",
    "ING": "Ingeniería",
    "Ingeniería": "Ingeniería"
}

MAP_TURNO = {
    "MAT": "Matutino",
    "Matutino": "Matutino",
    "VESP": "Vespertino",
    "Vespertino": "Vespertino"
}

MAP_CARRERA = {
    "Lic Psicologia": "Lic. en Psicología",
    "Ing Civil": "Ing. Civil"
}

# =========================
# FUNCIONES
# =========================
def limpiar_texto(col):
    return (
        col.astype(str)
        .str.strip()
        .replace("", pd.NA)
        .replace("N/A", pd.NA)
    )

def limpiar_fecha(col):
    return pd.to_datetime(col, errors="coerce", dayfirst=True)

# =========================
# PROCESO
# =========================
for archivo in glob.glob(f"{INPUT_DIR}/*.csv"):
    df = pd.read_csv(archivo)

    # Texto general
    columnas_texto = [
        "sexo", "nacionalidad", "colonia", "escuela_procedencia",
        "ubicacion_escuela_procedencia", "nivel", "turno", "carrera"
    ]

    for col in columnas_texto:
        df[col] = limpiar_texto(df[col])

    # Mapeos
    df["sexo"] = df["sexo"].map(MAP_SEXO)
    df["nacionalidad"] = df["nacionalidad"].map(MAP_NACIONALIDAD).fillna("Mexicana")
    df["nivel"] = df["nivel"].map(MAP_NIVEL)
    df["turno"] = df["turno"].map(MAP_TURNO)
    df["carrera"] = df["carrera"].replace(MAP_CARRERA)

    # Fecha
    df["fecha_nacimiento"] = limpiar_fecha(df["fecha_nacimiento"])

    # Guardar limpio
    nombre = os.path.basename(archivo)
    output_path = os.path.join(OUTPUT_DIR, nombre)

    df.to_csv(output_path, index=False, encoding="utf-8")

    print(f"✔ Archivo limpiado: {output_path}")

import csv
import os
import re
import unicodedata
from datetime import datetime

INPUT_FOLDER = "csv_vizcaya"
OUTPUT_FOLDER = "csv_vizcaya_limpios"
MASTER_FILE = "inscripciones_master_limpio.csv"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# =========================
# FUNCIONES AUXILIARES
# =========================

def quitar_acentos(texto: str) -> str:
    if texto is None:
        return ""
    texto = str(texto)
    return "".join(
        c for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )

def limpiar_texto(texto: str) -> str:
    if texto is None:
        return ""
    texto = str(texto).strip()
    texto = re.sub(r"\s+", " ", texto)
    return texto

def estandarizar_titulo(texto: str) -> str:
    texto = limpiar_texto(texto)
    if not texto:
        return ""
    palabras = texto.split(" ")
    resultado = []
    for p in palabras:
        if p.upper() in ["ING", "LIC", "MAT", "VESP", "UVA"]:
            resultado.append(p.upper())
        else:
            resultado.append(p.capitalize())
    return " ".join(resultado)

# =========================
# LIMPIEZAS ESPECÍFICAS
# =========================

def limpiar_sexo(sexo: str) -> str:
    sexo = limpiar_texto(sexo).upper()
    if sexo in ["M", "MASCULINO", "H", "HOMBRE"]:
        return "M"
    if sexo in ["F", "FEMENINO", "FEM", "MUJER"]:
        return "F"
    return "NA"

def limpiar_nacionalidad(nac: str) -> str:
    nac = limpiar_texto(nac)
    if nac == "" or nac.upper() in ["N/A", "NA"]:
        return "NA"
    nac_sin = quitar_acentos(nac).lower()
    if nac_sin in ["mexicana", "mexicano", "mexico", "mx"]:
        return "Mexicana"
    return estandarizar_titulo(nac)

def limpiar_colonia(col: str) -> str:
    col = limpiar_texto(col)
    if col == "":
        return "NA"
    col_sin = quitar_acentos(col).lower()
    if col_sin == "centro":
        return "Centro"
    return estandarizar_titulo(col)

def limpiar_nivel(nivel: str) -> str:
    nivel = limpiar_texto(nivel).upper()
    if nivel in ["LICENCIATURA", "LIC"]:
        return "Licenciatura"
    if nivel in ["INGENIERIA", "INGENIERÍA", "ING"]:
        return "Ingeniería"
    return "NA"
def limpiar_turno(turno: str) -> str:
    turno = limpiar_texto(turno).upper()
    if turno in ["MATUTINO", "MAT"]:
        return "Matutino"
    if turno in ["VESPERTINO", "VESP"]:
        return "Vespertino"
    return "NA"

def limpiar_ciclo(ciclo: str) -> str:
    ciclo = limpiar_texto(ciclo)
    if ciclo == "":
        return "NA"

    c = quitar_acentos(ciclo).lower()

    if c in ["enero-junio", "enero junio", "ene-jun", "ene jun"]:
        return "Enero-Junio"
    if c in ["agosto-diciembre", "agosto diciembre", "ago-dic", "ago dic"]:
        return "Agosto-Diciembre"
    if re.match(r"^\d{4}-[abAB]$", ciclo):
        return ciclo.upper()
    if "-" in ciclo:
        partes = ciclo.split("-")
        partes = [p.strip().capitalize() for p in partes]
        return "-".join(partes)

    return estandarizar_titulo(ciclo)

def limpiar_carrera(carrera: str) -> str:
    carrera = limpiar_texto(carrera)
    if carrera == "":
        return "NA"

    c = quitar_acentos(carrera).lower()

    if c in ["lic psicologia", "lic. psicologia", "lic psicología"]:
        return "Lic. en Psicología"
    if c in ["ing civil", "ing. civil"]:
        return "Ing. Civil"

    carrera = estandarizar_titulo(carrera)
    carrera = carrera.replace("Lic. En", "Lic. en")
    carrera = carrera.replace("Ing. En", "Ing. en")

    return carrera

def limpiar_fecha(fecha: str) -> str:
    fecha = limpiar_texto(fecha)
    if fecha == "":
        return "NA"

    formatos = ["%Y-%m-%d", "%d/%m/%Y", "%m-%d-%Y"]

    for f in formatos:
        try:
            dt = datetime.strptime(fecha, f)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue

    return "NA"

def limpiar_lugar(lugar: str) -> str:
    lugar = limpiar_texto(lugar)
    if lugar == "":
        return "NA"
    return estandarizar_titulo(lugar)

def limpiar_escuela(escuela: str) -> str:
    escuela = limpiar_texto(escuela)
    if escuela == "" or escuela.upper() in ["N/A", "NA"]:
        return "NA"
    return estandarizar_titulo(escuela)

def limpiar_ubicacion_escuela(ubicacion: str) -> str:
    ubicacion = limpiar_texto(ubicacion)
    if ubicacion == "":
        return "NA"
    return estandarizar_titulo(ubicacion)

def limpiar_matricula(m: str) -> str:
    m = limpiar_texto(m).upper()
    if m == "":
        return "NA"
    return m

def limpiar_tipo_ingreso(tipo: str) -> str:
    tipo = limpiar_texto(tipo).lower()
    if tipo == "":
        return "NA"

    mapa = {
        "nuevo": "Nuevo",
        "repetidor": "Repetidor",
        "reinscrito": "Reinscrito",
        "equivalencia": "Equivalencia"
    }

    return mapa.get(tipo, estandarizar_titulo(tipo))

# =========================
# LIMPIEZA DE FILA
# =========================

def limpiar_fila(row: dict, anio_inscripcion: int) -> dict:
    return {
        "anio_inscripcion": anio_inscripcion,
        "matricula": limpiar_matricula(row.get("matricula", "")),
        "sexo": limpiar_sexo(row.get("sexo", "")),
        "nacionalidad": limpiar_nacionalidad(row.get("nacionalidad", "")),
        "lugar_nacimiento": limpiar_lugar(row.get("lugar_nacimiento", "")),
        "fecha_nacimiento": limpiar_fecha(row.get("fecha_nacimiento", "")),
        "tipo_ingreso": limpiar_tipo_ingreso(row.get("tipo_ingreso", "")),
        "colonia": limpiar_colonia(row.get("colonia", "")),
        "escuela_procedencia": limpiar_escuela(row.get("escuela_procedencia", "")),
        "ubicacion_escuela_procedencia": limpiar_ubicacion_ubicacion(row.get("ubicacion_escuela_procedencia", "")),
        "modalidad": row.get("modalidad", ""),
        "nivel": limpiar_nivel(row.get("nivel", "")),
        "carrera": limpiar_carrera(row.get("carrera", "")),
        "turno": limpiar_turno(row.get("turno", "")),
        "ciclo": limpiar_ciclo(row.get("ciclo", ""))
    }

# OJO: corregimos un typo
def limpiar_ubicacion_ubicacion(ubicacion: str) -> str:
    return limpiar_ubicacion_escuela(ubicacion)

# =========================
# PROCESAMIENTO
# =========================

def obtener_anio_desde_nombre(nombre_archivo: str) -> int:
    # Ej: inscripciones_2017.csv
    match = re.search(r"(\d{4})", nombre_archivo)
    if match:
        return int(match.group(1))
    return 0

def limpiar_y_unir():
    columnas_finales = [
        "anio_inscripcion",
        "matricula",
        "sexo",
        "nacionalidad",
        "lugar_nacimiento",
        "fecha_nacimiento",
        "tipo_ingreso",
        "colonia",
        "escuela_procedencia",
        "modalidad",
        "ubicacion_escuela_procedencia",
        "nivel",
        "carrera",
        "turno",
        "ciclo"
    ]

    master_path = os.path.join(OUTPUT_FOLDER, MASTER_FILE)

    with open(master_path, mode="w", newline="", encoding="utf-8-sig") as master_out:
        master_writer = csv.DictWriter(master_out, fieldnames=columnas_finales)
        master_writer.writeheader()

        for file in os.listdir(INPUT_FOLDER):
            if not file.endswith(".csv"):
                continue

            input_path = os.path.join(INPUT_FOLDER, file)
            anio = obtener_anio_desde_nombre(file)

            output_path = os.path.join(
                OUTPUT_FOLDER,
                file.replace(".csv", "_limpio.csv")
            )

            # Limpieza por archivo (y también se mete al master)
            with open(input_path, mode="r", encoding="utf-8") as f_in:
                reader = csv.DictReader(f_in)

                with open(output_path, mode="w", newline="", encoding="utf-8-sig") as f_out:
                    writer = csv.DictWriter(f_out, fieldnames=columnas_finales)
                    writer.writeheader()

                    for row in reader:
                        fila = limpiar_fila(row, anio)

                        writer.writerow(fila)
                        master_writer.writerow(fila)

            print(f" Limpio por año: {output_path}")

    print(f"\n CSV MASTER generado: {master_path}")

if __name__ == "__main__":
    limpiar_y_unir()

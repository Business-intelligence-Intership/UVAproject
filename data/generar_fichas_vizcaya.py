import csv
import random
from datetime import datetime, timedelta
import os

# =========================
# CONFIGURACIÓN
# =========================
ANIOS = {
    2018: 644,
    2019: 1208,
    2020: 1056,
    2021: 1400,
    2022: 1585,
    2023: 1250,
    2024: 1418,
    2025: 1561
}

CARRERAS = [
    "Ing. Civil",
    "Ing. en Procesos de Manufactura",
    "Lic. en Admin. de Empresas",
    "Lic. en Arquitectura",
    "Lic. en Contabilidad",
    "Lic. en Criminología",
    "Lic. en Derecho",
    "Lic. en Diseño de Modas",
    "Lic. en Educación",
    "Lic. en Enfermería",
    "Lic. en Fisioterapia",
    "Lic. en Gastronomía",
    "Lic. en Nutrición",
    "Lic. en Odontología",
    "Lic. en Psicología"
]

TIPO_INGRESO = ["Nuevo", "Repetidor", "Reinscrito", "Equivalencia"]
SEXO_SUCIO = ["M", "F", "Masculino", "Femenino", "H", "Fem", ""]
NACIONALIDAD_SUCIA = ["Mexicana", "mexicano", "MX", "México", "N/A", ""]
COLONIAS = ["Centro", "centro", "CENTRO", "Itzimná", "Chuburná", "Francisco de Montejo", ""]

NIVELES = ["Licenciatura", "Ingeniería", "LIC", "ING"]
TURNOS = ["Matutino", "Vespertino", "MAT", "VESP"]
CICLOS = ["Enero-Junio", "Agosto-Diciembre", "2023-A", "2024-B"]

ESCUELAS = [
    "Preparatoria Estatal No. 1",
    "CBTIS 95",
    "CONALEP Mérida",
    "Prepa Abierta",
    "N/A",
    ""
]

UBICACIONES_ESCUELA = [
    "Mérida, Yucatán",
    "Kanasín",
    "Umán",
    "Tizimín",
    ""
]

os.makedirs("csv_vizcaya", exist_ok=True)

# =========================
# FUNCIONES
# =========================
def fecha_nacimiento_sucia():
    start = datetime(1995, 1, 1)
    end = datetime(2005, 12, 31)
    fecha = start + timedelta(days=random.randint(0, (end - start).days))
    formatos = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%m-%d-%Y"
    ]
    return fecha.strftime(random.choice(formatos))

def matricula_sucia(anio):
    base = f"UVA{anio}"
    return base + str(random.randint(1000, 9999))

# =========================
# GENERACIÓN
# =========================
for anio, total in ANIOS.items():
    filename = f"csv_vizcaya/inscripciones_{anio}.csv"
    
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        writer.writerow([
            "matricula",
            "sexo",
            "nacionalidad",
            "lugar_nacimiento",
            "fecha_nacimiento",
            "tipo_ingreso",
            "colonia",
            "escuela_procedencia",
            "ubicacion_escuela_procedencia",
            "nivel",
            "carrera",
            "turno",
            "ciclo"
        ])
        
        for _ in range(total):
            writer.writerow([
                matricula_sucia(anio),
                random.choice(SEXO_SUCIO),
                random.choice(NACIONALIDAD_SUCIA),
                random.choice(["Mérida", "Valladolid", "Tizimín", "Cancún", ""]),
                fecha_nacimiento_sucia(),
                random.choice(TIPO_INGRESO),
                random.choice(COLONIAS),
                random.choice(ESCUELAS),
                random.choice(UBICACIONES_ESCUELA),
                random.choice(NIVELES),
                random.choice(CARRERAS + ["Lic Psicologia", "Ing Civil"]),
                random.choice(TURNOS),
                random.choice(CICLOS)
            ])

    print(f"CSV generado: {filename}")
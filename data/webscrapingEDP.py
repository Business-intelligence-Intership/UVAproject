import googlemaps
import time
import os
import csv
from dotenv import load_dotenv

# =========================
# CONFIG
# =========================
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("❌ No se encontró GOOGLE_API_KEY en el .env")

gmaps = googlemaps.Client(key=API_KEY)

# Centro de Mérida + radio que cubre Yucatán
YUCATAN_LOCATION = (20.967, -89.624)
YUCATAN_RADIUS = 200_000  # 200 km

# =========================
# HELPERS YUCATÁN
# =========================
def en_bbox_yucatan(lat, lng):
    return 19.4 <= lat <= 21.7 and -90.5 <= lng <= -87.3

def texto_indica_yucatan(texto):
    texto = texto.lower()
    claves = [
        "yucatán", "yucatan", "mérida", "merida",
        "progreso", "ticul", "valladolid", "tizimin",
        "umán", "kanasin", "hunucma"
    ]
    return any(c in texto for c in claves)

def extraer_estado(componentes):
    for c in componentes:
        if "administrative_area_level_1" in c["types"]:
            return c["long_name"]
    return ""

def extraer_municipio(componentes):
    for c in componentes:
        if any(t in c["types"] for t in [
            "locality",
            "administrative_area_level_2",
            "administrative_area_level_3"
        ]):
            return c["long_name"]
    return ""

# =========================
# SCORING
# =========================
def score_resultado(r, nombre_original):
    score = 0
    loc = r["geometry"]["location"]
    lat, lng = loc["lat"], loc["lng"]

    if en_bbox_yucatan(lat, lng):
        score += 2

    texto = (r.get("formatted_address", "") + " " + nombre_original).lower()
    if texto_indica_yucatan(texto):
        score += 1

    return score

def elegir_mejor_resultado(results, nombre_original):
    mejor = None
    mejor_score = -1

    for r in results:
        s = score_resultado(r, nombre_original)
        if s > mejor_score:
            mejor = r
            mejor_score = s

    return mejor

# =========================
# FILA VACÍA
# =========================
def fila_vacia(nombre):
    return {
        "nombre_original": nombre,
        "nombre_google": "",
        "direccion": "",
        "municipio": "",
        "estado": "",
        "lat": "",
        "lng": "",
        "es_yucatan": False,
        "criterio": "",
        "place_id": ""
    }

# =========================
# BÚSQUEDA
# =========================
def buscar_escuela(nombre):
    print(f"🔍 Buscando: {nombre}")

    try:
        response = gmaps.places(
            query=f"{nombre}, México",
            location=YUCATAN_LOCATION,
            radius=YUCATAN_RADIUS
        )
    except Exception as e:
        print(f"⚠️ Error en búsqueda Places: {e}")
        return fila_vacia(nombre)

    if not response.get("results"):
        return fila_vacia(nombre)

    lugar = elegir_mejor_resultado(response["results"], nombre)
    if not lugar:
        return fila_vacia(nombre)

    place_id = lugar["place_id"]

    try:
        details = gmaps.place(
            place_id=place_id,
            fields=[
                "name",
                "formatted_address",
                "address_component",
                "geometry"
            ]
        )
    except Exception as e:
        print(f"⚠️ Error en details: {e}")
        return fila_vacia(nombre)

    r = details.get("result", {})
    componentes = r.get("address_component", [])
    geometry = r.get("geometry", {}).get("location", {})

    lat = geometry.get("lat", "")
    lng = geometry.get("lng", "")

    estado = extraer_estado(componentes)
    municipio = extraer_municipio(componentes)

    razones = []
    if estado == "Yucatán":
        razones.append("estado")
    if lat != "" and lng != "" and en_bbox_yucatan(lat, lng):
        razones.append("coordenadas")
    if texto_indica_yucatan(nombre + " " + r.get("formatted_address", "")):
        razones.append("texto")

    return {
        "nombre_original": nombre,
        "nombre_google": r.get("name", ""),
        "direccion": r.get("formatted_address", ""),
        "municipio": municipio,
        "estado": estado,
        "lat": lat,
        "lng": lng,
        "es_yucatan": bool(razones),
        "criterio": ",".join(razones),
        "place_id": place_id
    }

# =========================
# PROCESO
# =========================
def procesar(lista):
    data = []
    for nombre in lista:
        try:
            data.append(buscar_escuela(nombre))
            time.sleep(0.3)
        except Exception as e:
            print(f"❌ Error grave con {nombre}: {e}")
            data.append(fila_vacia(nombre))
    return data

def guardar_csv(data):
    with open("escuelas_clasificadas_final_2.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    escuelas = [
<<<<<<< HEAD
    "COBAY CACALCHEN",
    "PREPARATORIA ESTATAL #10 RUBÉN H. RODRÍGUEZ MOGUEL",
    "UNIVERSIDAD VIZCAYA DE LAS AMÉRICAS",
    "ACUERDO 286",
    "ANTONIO BETANCOURT PEREZ",
    "ALIANZ COMUNIDAD ESTUDIANTIL",
    "ALIANZA DE CAMIONEROS",
    "PLANTEL AZTECA",
    "BACHILLERATO GENERAL CON FORMACION LABORAL BASICA",
    "BACHILLERATO EN LINEA UADY",
    "BACHILLERES AMERICAS",
    "BENITO JUAREZ DE TANTOYUCA VERACRUZ",
    "BETANCOURT -BRISAS",
    "COLEGIO BLAS PASCAL",
=======
   "COBAY CACALCHEN",
   "PREPARATORIA ESTATAL #10 RUBÉN H. RODRÍGUEZ MOGUEL",
   "UNIVERSIDAD VIZCAYA DE LAS AMÉRICAS",
   "ACUERDO 286",
   "ALIANZA DE CAMIONEROS",
   "BACHILLERATO EN LINEA UADY",
   "BETANCOURT -BRISAS",    
>>>>>>> Valeria
    "FELIPE ESCALANTE RUZ - BRISAS",
    "BACHILLERATO COMUNITARIO SAMAHIL",
    "COBAY BUCTOZTZ",
    "COBAY TIXKOKOB",
<<<<<<< HEAD
    "CBTIS 111  CANCUN",
=======
>>>>>>> Valeria
    "CBETIS 120",
    "CBTIS 80",
    "COLEGIO AMERICANO",
    "COBACH COZUMEL",
    "COBAY CHENKU",
    "COBAY HOMUN",
    "COBAY SOTUTA",
    "COBAY TZUCACAB",
    "CBTA 13  XMATKUIL",
    "COBAY YAXCABA",
    "PREPARATORIA ABIERTA CALAFIA",
<<<<<<< HEAD
    "VICTOR J. MANZANILLA J. -CANSAHCAB",
    "CBTIS 28- COZUMEL",
    "COLEGIO BENITO JUAREZ GARCIA",
    "Centro de Bachillerato Tecnologico Agropecuario",
=======
    "CBTIS 28 COZUMEL",
    "CENTRO DE BACHILLERATO TECNOLOGICO AGROPECUARIO",
>>>>>>> Valeria
    "CBTA 165",
    "CBTA 178",
    "CBTIS 95",
    "CENTRO DE BACHILLERATO TECNOLOGICO INDUSTRIAL Y DE SERVICIOS",
    "CARLOS CASTILLO PERAZA",
<<<<<<< HEAD
    "CENTRO EDUCATIVO SIGLO XXI",
=======
>>>>>>> Valeria
    "CECYTE",
    "CECYTE PLANTEL POMUCH",
    "CECYTE QUINTANA ROO",
<<<<<<< HEAD
    "CECYTE 16 TABASCO",
    "CEC Y TES",
    "CEDART Ermilo Abreu Gómez",
    "CEEAC",
    "CELA",
    "CENTRO EDUCATIVO MARIA GONZALEZ PALMA",
    "Centennial Collegiate Vocational Institute",
    "CENTRO ESCOLAR ROCHAVI",
    "CERT TICUL",
    "CESMAC",
    "CETESC",
    "CETIS 112",
    "Centro de Estudios Tecnológicos del Mar No 17",
    "Colegio de Estudios Universitarios del Mayab",
    "COBAY CHOLUL",
    "CEMA",
    "UNIVERSIDAD CNCI",
    "COBAY CELESTUN",
    "Colegio de Bachilleres del Estado de Campeche",
    "COBACAM-CAMPECHE",
    "COLEGIO DE BACHILLERES DE BAJA CALIFORNIA SUR",
    "COBACH CHIAPAS",
    "COLEGIO DE BACHILLERES QUINTANA ROO",
    "COLEGIO BACHILLERES TABASCO",
    "COBATAB",
    "COLEGIO DE BACHILLERES No.8 TABASCO",
=======
    "CEDART Ermilo Abreu Gómez",
    "CEEAC",
    "CEIC PLAYA DEL CARMEN",
    "CENTRO EDUCATIVO MARIA GONZALEZ PALMA",
    "COREM MERIDA",
    "CENTRO ESCOLAR ROCHAVI",
    "CETIS 112",
    "CETIS 134",
    "CETIS 68",
    "COBAY CHOLUL",
    "CEMA",
    "UNIVERSIDAD CNCI",
    "Colegio de Bachilleres del Estado de Campeche",
    "COBACAM-CAMPECHE",
    "COLEGIO DE BACHILLERES CHIAPAS",
    "COLEGIO DE BACHILLERES QUINTANA ROO",
    "COLEGIO BACHILLERES TABASCO",
    "COLEGIO BACHILLERES DE TABASCO 46",
>>>>>>> Valeria
    "COBAY PROGRESO",
    "COBAY 5",
    "COBAY ACANCEH",
    "COBAY BACA",
    "COBAY CAUCEL",
    "COLEGIO DE BACHILLERES PLANTEL COZUMEL",
    "COBAY DZIDZANTUN",
    "COBAY KANASIN",
    "COBAY KIMBILA",
    "COBAY KINCHIL",
    "COBAY CHICXULUB PUEBLO",
    "COBAY SANTA ROSA",
    "COBAY TEKIT",
    "COBAY TECOH",
    "COBAY TICUL",
    "COBAY UMAN",
    "COBAY XOCLAN",
<<<<<<< HEAD
    "PLANTEL COBAY SAN JOSE TZAL",
    "COBAY TEABO",
    "COBAY TIZIMIN",
    "COLEGIO DE BACHILLERES, PLANTEL JMM",
=======
>>>>>>> Valeria
    "COBAY SEYE",
    "COLEGIO MESOAMERICANO",
    "COMPLUTENSE CENTRO INTEGRADO, INC. SAN LORENZO",
<<<<<<< HEAD
=======
    "CONALEP PLANTEL COZUMEL",
    "COLEGIO NACIONAL DE EDUCACIÓN PROFESIONAL TÉCNICA",
>>>>>>> Valeria
    "CONALEP MERIDA",
    "CONALEP QUINTANA ROO",
    "CONRADO MENENDEZ DIAZ",
<<<<<<< HEAD
    "CONSUELO ZAVALA",
=======
    "CRISMAR",
    "CONALEP TIZIMIN",
>>>>>>> Valeria
    "COBAY CUZAMA",
    "CUDEC",
    "CENTRO UNIVERSITARIO FELIPE CARRILLO PUERTO",
<<<<<<< HEAD
    "CUM",
    "COLEGIO YUCATAN",
    "DAVID ALAFARO SIQUEIROS MIRAFLORES",
    "EBAO",
    "INSTITUTO ECOLE JOHNSON",
    "EDUCACION  INTEGRAL Y ACTIVA EDAI",
    "COLEGIO EDUCACION Y PATRIA",
    "ELIGIO ANCONA",
    "ELOISA PATRONN ROSADO",
    "EMSAD 07 EL DESENGAÑO",
    "ENEP UNAM SEP",
=======
    "COLEGIO YUCATAN",
    "DAVID ALAFARO SIQUEIROS MIRAFLORES",
    "COLEGIO EDUCACION Y PATRIA",
    "ELIGIO ANCONA",
    "ELOISA PATRONN ROSADO",
    "ENP4 VIDAL CASTAÑEDA Y NAJERA",
>>>>>>> Valeria
    "ESCUELA PREPARATORIA JOSE DOLORES RODRIGUEZ TAMAYO",
    "PREPARATORIA ESTATAL NUM. 10",
    "PREPARATORIA ESTATAL #6 ALIANZA DE CAMIONEROS",
    "FRANCISCO DE MONTEJO Y LEON",
    "GONZALO CAMARA ZAVALA",
    "COBAY HUNUCMA",
    "INSTITUTO FELTON",
    "INCI - ALEMAN",
<<<<<<< HEAD
    "INEVE",
    "INSTITUTO COMERCIAL BANCARIO",
    "Instituto David Alfaro",
=======
    "INSTITUTO PATRIA",
    "INSTITUTO COMERCIAL BANCARIO",
>>>>>>> Valeria
    "INSTITUTO MEXICO",
    "ITECOS",
    "JOSE VASCONCELOS",
    "PREPARATORIA JUVENTUS",
<<<<<<< HEAD
    "cobay komchen",
    "PREPARATRIA LAFAYETTE",
    "LUIS ALVAREZ BARRET",
    "MAHATMA GANDHI",
    "CETMAR-PROGRESO",
=======
    "COBAY KOMCHEN",
    "LUIS PASTEUR - CAMPECHE",
    "LIBERTADES DE AMERICA",
    "LUIS ALVAREZ BARRET",
    "MAHATMA GANDHI",
    "CETMAR-PROGRESO",
    "COLEGIA MANUEL SANCHEZ MARMOL",
>>>>>>> Valeria
    "MANUEL CRESCENCIO REJON",
    "MEXICANA DEL MAYAB",
    "PREPARATORIA MODELO",
    "CENTRO EDUCATIVO MOTULEÑO",
    "PREPARATORIA MUNA",
<<<<<<< HEAD
    "COBAY PLANTEL PETO",
    "PREPA ACANCEH",
    "PREPARATORIA BENITO JUAREZ CDAD DEL CARMEN",
    "PREPA ABIERTA",
    "PREPARATORIA LIBRE",
    "PREPA LIBRE SEP",
    "PREPARATORIA ESTATAL No. 8",
    "PREPARATORIA ESTATAL CTM # 3",
    "PREPA 1",
    "PREPARATORIA 11",
    "PREPARATORIA ESTATAL 3",
    "PREPA 4 CANSAHCAB",
    "PREPARATORIA #5 AGUSTIN FRANCO VILLANUEVA",
    "PREPA 7",
    "PREPARATORIA NO. 8",
    "VICTOR MANUEL CERVERA PACHECO",
    "PREPARATORIA ESTATAL 2",
    "PREPARATORIA MEXICO",
    "PREPARATORIA MIGUEL ANGEL",
    "PREPARATORIA PROGRESO",
    "Preparatoria de Tahdzibichen",
    "PREPARATORIA YUCATAN",
    "PREPARATORIA 1 UADY",
    "PREPARATORIA 3 UADY",
    "PREPARATORIA 4",
    "PRONACE",
    "REPUBLICA DE MEXICO"
=======
    "UNIVERSIDAD DE MUNDO MAYA"
>>>>>>> Valeria
    ]

    data = procesar(escuelas)
    guardar_csv(data)
    print("✅ CSV generado correctamente")

        
    
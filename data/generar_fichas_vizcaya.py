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

CARRERAS_CUATRI = [
    "Ingeniería Civil",
    "Administración de Empresas",
    "Arquitectura",
    "Contabilidad",
    "Criminología",
    "Derecho",
    "Diseño de Modas",
    "Educación",
    "Enfermería",
    "Fisioterapia",
    "Gastronomía",
    "Nutrición",
    "Psicología"
]

CARRERA_SEMESTRE = [
    "Odontología", 
]

TIPO_INGRESO = ["Nuevo", "Repetidor", "Reinscrito", "Equivalencia"]

SEXO_SUCIO = ["M", "F", "Masculino", "Femenino", "H", "Fem", ""]

NACIONALIDAD_SUCIA = ["Mexicana", "mexicano", "MX", "México", "N/A", ""]

COLONIAS = [
    "Centro",
    "Altabrisa",
    "Chuburná de Hidalgo",
    "Francisco de Montejo",
    "García Ginerés",
    "Itzimná",
    "Pensiones",
    "Montecristo",
    "Montes de Amé",
    "San Ramón Norte",
    "San Ramón Sur",
    "México",
    "Miguel Alemán",
    "Jardines del Norte",
    "Campestre",
    "Xoclán",
    "Wallis",
    "Salvador Alvarado Sur",
    "Ciudad Caucel",
    "Las Américas",
    "Dzityá",
    "Temozón Norte",
    "Juan Pablo II",
    "Bojórquez",
    "Mayapán",
    "Dolores Otero",
    "Emiliano Zapata Sur",
    "Nueva Kukulcán",
    "Mulsay",
    "Brisas",
    "San Antonio Kaua",
    ""
]

NIVELES = ["Licenciatura", "Ingeniería", "LIC", "ING"]

TURNOS = ["Matutino", "Vespertino", "MAT", "VESP"]

CICLO_SEMESTRAL = ["Enero-Junio", "Agosto-Diciembre"]

CICLO_CUATRIMESTRAL = ["Enero-Abril", "Mayo-Agosto", "Septiembre-Diciembre"]

ESCUELAS = [
    "COBAY CACALCHEN",
    "PREPARATORIA ESTATAL #10 RUBÉN H. RODRÍGUEZ MOGUEL",
    "UNIVERSIDAD VIZCAYA DE LAS AMÉRICAS",
    "ACUERDO 286",
    "ALIANZ COMUNIDAD ESTUDIANTIL",
    "ALIANZA DE CAMIONEROS",
    "PLANTEL AZTECA",
    "BACHILLERATO EN LINEA UADY",
    "BACHILLERES AMERICAS",
    "BETANCOURT - BRISAS",
    "FELIPE ESCALANTE RUZ - BRISAS",
    "BACHILLERATO COMUNITARIO SAMAHIL",
    "COBAY BUCTOZTZ",
    "COBAY TIXKOKOB",
    "CBTIS 111 CANCUN",
    "CBETIS 120",
    "CBTIS 126 CAMPECHE",
    "CBTIS 80",
    "COLEGIO AMERICANO",
    "COBACH COZUMEL",
    "COBAY CHENKU",
    "COBAY HOMUN",
    "COBAY SOTUTA",
    "COBAY TZUCACAB",
    "CBTA 13 XMATKUIL",
    "COBAY YAXCABA",
    "COBAY ABALA",
    "PREPARATORIA ABIERTA CALAFIA",
    "VICTOR J. MANZANILLA J. - CANSAHCAB",
    "CBTIS 28 COZUMEL",
    "COLEGIO BENITO JUAREZ GARCIA",
    "CENTRO DE BACHILLERATO TECNOLOGICO AGROPECUARIO",
    "CBTA 165",
    "CBTA IZAMAL 185",
    "CBTIS 95",
    "CBTIS 120 MÉRIDA",
    "CARLOS CASTILLO PERAZA",
    "UNIVERSIDAD AUTONOMA DEL CARMEN",
    "CENTRO EDUCATIVO SIGLO XXI",
    "CECYTE",
    "CECYTE QUINTANA ROO",
    "CEC Y TES",
    "CEDART ERMILO ABREU GÓMEZ",
    "CEEAC",
    "CEIC PLAYA DEL CARMEN",
    "CELA",
    "CENTRO EDUCATIVO MARIA GONZALEZ PALMA",
    "COREM MERIDA",
    "CENTENNIAL COLLEGIATE VOCATIONAL INSTITUTE",
    "CENTRO ESCOLAR ROCHAVI",
    "CESMAC",
    "CETESC",
    "CETIS 112",
    "CETIS 134",
    "CETIS 68",
    "CENTRO DE ESTUDIOS TECNOLÓGICOS DEL MAR No 17",
    "COLEGIO DE ESTUDIOS UNIVERSITARIOS DEL MAYAB",
    "COBAY CHOLUL",
    "CEMA",
    "UNIVERSIDAD CNCI",
    "COBAY CELESTUN",
    "COLEGIO DE BACHILLERES DEL ESTADO DE CAMPECHE",
    "COLEGIO DE BACHILLERES CHIAPAS",
    "COLEGIO DE BACHILLERES QUINTANA ROO",
    "COLEGIO BACHILLERES TABASCO",
    "COLEGIO BACHILLERES DE TABASCO 46",
    "COBATAB",
    "COLEGIO DE BACHILLERES No. 8 TABASCO",
    "COBAY PROGRESO",
    "COBAY 5",
    "COBAY ACANCEH",
    "COBAY BACA",
    "COBAY CAUCEL",
    "COLEGIO DE BACHILLERES PLANTEL COZUMEL",
    "COBAY DZIDZANTUN",
    "COBAY HALACHO",
    "COBAY KANASIN",
    "COBAY KIMBILA",
    "COBAY KINCHIL",
    "COLEGIO DE BACHILLERES DE YUCATAN",
    "COBAY CHICXULUB PUEBLO",
    "COBAY SANTA ROSA",
    "COBAY TEKIT",
    "COBAY TECOH",
    "COBAY TICUL",
    "COBAY UMAN",
    "COBAY VALLADOLID",
    "COBAY XOCLAN",
    "PLANTEL COBAY SAN JOSE TZAL",
    "COBAY TEABO",
    "COBAY TIZIMIN",
    "COLEGIO DE BACHILLERES PLANTEL JMM",
    "COBAY SEYE",
    "COLEGIO MESOAMERICANO",
    "COLEGIO DEL GOLFO DE MERIDA",
    "COMPLUTENSE CENTRO INTEGRADO, INC. SAN LORENZO",
    "COLEGIO NACIONAL DE EDUCACIÓN PROFESIONAL TÉCNICA",
    "CONALEP MERIDA",
    "CONRADO MENENDEZ DIAZ",
    "COBAY CUZAMA",
    "CENTRO UNIVERSITARIO FELIPE CARRILLO PUERTO",
    "CUM",
    "CENTRO UNIVERSITARIO MONTEJO",
    "COLEGIO YUCATAN",
    "DAVID ALFARO SIQUEIROS MIRAFLORES",
    "EDUCACION INTEGRAL Y ACTIVA EDAI",
    "COLEGIO EDUCACION Y PATRIA",
    "ELIGIO ANCONA",
    "EMSAD 07 EL DESENGAÑO",
    "ENEP UNAM SEP",
    "ESCUELA PREPARATORIA JOSE DOLORES RODRIGUEZ TAMAYO",
    "PREPARATORIA ESTATAL NUM. 10",
    "FRANCISCO DE MONTEJO Y LEON",
    "FRANCISCO REPETO MILAN",
    "GONZALO CAMARA ZAVALA",
    "COBAY HUNUCMA",
    "IBCEY",
    "INSTITUTO FELTON",
    "IMEI - CIUDAD DE MEXICO",
    "INCI - ALEMAN",
    "INEVE",
    "INSTITUTO PATRIA",
    "INSTITUTO COMERCIAL BANCARIO",
    "INSTITUTO DAVID ALFARO",
    "INSTITUTO MEXICO",
    "JOSE MARIA MORELOS Y PAVON",
    "JOSE VASCONCELOS",
    "JOSEFINA ROSADO DE PATRON",
    "PREPARATORIA JUVENTUS",
    "COBAY KOMCHEN",
    "LUIS PASTEUR - CAMPECHE",
    "LA SALLE BOULLEWARES",
    "PREPARATORIA LAFAYETTE",
    "LUIS ALVAREZ BARRET",
    "MAHATMA GANDHI",
    "CETMAR-PROGRESO",
    "COLEGIO MANUEL SANCHEZ MARMOL",
    "MANUEL CRESCENCIO REJON",
    "MEXICANA DEL MAYAB",
    "PREPARATORIA MODELO",
    "PREPARATORIA MUNA",
    "UNIVERSIDAD DE MUNDO MAYA",
    "COBAY PLANTEL PETO",
    "PREPARATORIA 7",
    "PREPA ACANCEH",
    "PREPA ABIERTA",
    "PREPARATORIA LIBRE",
    "PREPA LIBRE SEP",
    "PREPARATORIA ESTATAL No. 8",
    "PREPARATORIA ESTATAL CTM #3",
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
    "PREPARATORIA DE TAHDZIBICHEN",
    "PREPARATORIA YUCATAN",
    "PREPARATORIA 1 UADY",
    "PREPARATORIA 3 UADY",
    "PREPARATORIA 4",
    "PREPARATORIA ESTATAL No. 9",
    "PRONACE",
    "REPUBLICA DE MEXICO",
    "RICARDO FLORES MAGÓN",
    "ROGERS HALL",
    "SERAPIO RENDÓN",
    "SALVADOR ALVARADO",
    "COLEGIO SAN AGUSTIN",
    "SIGLO XXI",
    "SERVICIO NACIONAL DE BACHILLERATO EN LINEA",
    "COBAY TEKAX",
    "UNIVERSIDAD TECMILENIO",
    "TELEBACHILLERATO",
    "COBAY TICUL",
    "JOSE DOLORES RODRIGUEZ TICUL",
    "COBAY TIXPEUAL",
    "UNACAR - CAMPUS II",
    "UABIC",
    "PREPARATORIA 2 UADY",
    "SAN AGUSTIN",
    "UNIVERSIDAD MEXICO AMERICANA DEL NORTE A.C.",
    "UPAV VERACRUZ",
    "UPP PREPA",
    "UVM",
    "ESCUELA NACIONAL PREPARATORIA 4 VIDAL CASTAÑEDA Y"
]

MODALIDAD = [
    "Escolarizada",
    "Mixto/Sabatino"
]

UBICACIONES_ESCUELA = {
"COBAY CACALCHEN": "Calle 19 91, Ciudad Ninguno, Cacalchén, Yucatán. Cp. 97460",
"PREPARATORIA ESTATAL #10 RUBÉN H. RODRÍGUEZ MOGUEL": "Calle 59, s/n 102-A y 106, Cd Caucel, 97314 Mérida, Yuc.",
"UNIVERSIDAD VIZCAYA DE LAS AMÉRICAS": "Calle 33 #140 Entre calle 20 A y 22 Col, Chuburná de Hidalgo, 97205 Mérida, Yuc.",
"ACUERDO 286": "NA",
"ALIANZ COMUNIDAD ESTUDIANTIL": "Calle 24 No 318 y 320, San Pedro Cholul, 97138 Mérida, Yuc.",
"ALIANZA DE CAMIONEROS": "C. 64 602, entre 75, 97000 Mérida, Yucatán",
"PLANTEL AZTECA": "Calle 23 s/n x 44a y 44b CCT 31EBH0004B, Mérida, Mexico, 97219",
"BACHILLERATO EN LINEA UADY": "NA",
"BACHILLERES AMERICAS": "Boulevard Benito Juárez 1404, Monclova, Coahuila de Zaragoza.",
"BETANCOURT - BRISAS": "Calle 25 S/N, Brisas del Pasaje, 97144 Mérida, Yuc.",
"FELIPE ESCALANTE RUZ - BRISAS": "97115 Mérida, Yucatán·",
"BACHILLERATO COMUNITARIO SAMAHIL": "97810 Samahil, Yuc.",
"COBAY BUCTOZTZ": "Calle 4, 21 Y 25, C. 4 SN, Centro, 97620 Buctzotz, Yucatán",
"COBAY TIXKOKOB": "97470 Tixkokob, Yucatán",
"CBTIS 111 CANCUN": "Av. Chichen-Itza Supermanzana 1, 77500 Cancún, Q.R.",
"CBETIS 120": "C. 13 101 por 60, 97205 Mérida, Yucatán",
"CBTIS 126 CAMPECHE": "24902, Calle 22-A 4100, Fátima, 24902 Calkiní, Camp.",
"CBTIS 80": "Calle 27 369, Edesio Carrillo Puerto, 97430 Motul de Carrillo, 97430",
"COLEGIO AMERICANO": "C. 72 499, Barrio de Santiago, Centro, 97000 Mérida, Yuc.",
"COBACH COZUMEL": "50 Avenida Sur, C. 27 Sur, San Miguel I, 77666 Cozumel, Q.R.",
"COBAY CHENKU": "Calle 32, Por Calle 25 y 27 SN, Residencial del Nte, 97219 Mérida, Yuc.",
"COBAY HOMUN": "97580 Homún, Yucatán",
"COBAY SOTUTA": "Calle 20 x 11 carretera a Tibolón, 40 X 11, 97690 Sotuta, Yucatán",
"COBAY TZUCACAB": "C. 30, 97960 Tzucacab, Yuc.",
"CBTA 13 XMATKUIL": "Ex-Hacienda Xmatkuil A.P. 970 Xmatkuil, 97139 Mérida, Yuc.",
"COBAY YAXCABA": "C. 22, 97920 Yaxcabá, Yuc.",
"COBAY ABALA": "Unnamed Road, 97825 Abalá, Yuc.",
"PREPARATORIA ABIERTA CALAFIA": "CALLE DEL BARRO, Av. Poblado Islas Agrarias # 1201, 21600 Mexicali, B.C.",
"VICTOR J. MANZANILLA J. - CANSAHCAB": "Calle 20 S/N, Cansahcab Centro, 97410 Cansahcab, Yuc.",
"CBTIS 28 COZUMEL": "Antonio González Fernández. 600, 10 de Abril, 77622 Cozumel, Q.R.",
"COLEGIO BENITO JUAREZ GARCIA": "C. 107, Santa Rosa, 97279 Mérida, Yuc.",
"CENTRO DE BACHILLERATO TECNOLOGICO AGROPECUARIO": "97315 Mérida, Yucatán",
"CBTA 165": "C. 30 102, Guadalupe, 97540 Izamal, Yuc.",
"CBTA IZAMAL 185": "C. 30 102, Guadalupe, 97540 Izamal, Yuc.",
"CBTIS 95": "Calle 18 No. 300-X 49, Salvador Alvarado Sur, 97190 Mérida, Yuc.",
"CBTIS 120 MÉRIDA": "C. 13 101 por 60, Loma Bonita, 97205 Mérida, Yuc.",
"CARLOS CASTILLO PERAZA": "Calle 51, Francisco de Montejo, Mérida, Yucatán",
"UNIVERSIDAD AUTONOMA DEL CARMEN": "C. 56 4, Benito Juárez, 24180 Cdad. del Carmen, Camp.",
"CENTRO EDUCATIVO SIGLO XXI": "C. 21 216, entre 60 Y 62, Zona Dorada II, 97226 Mérida, Yuc.",
"CECYTE": "Cl. 143 314, Emiliano Zapata Sur L, 97297 Mérida, Yuc.",
"CECYTE QUINTANA ROO": "C. 4 Pte. s/n, Maya Pax, Mayapax, 77780 Tulum, Q.R.",
"CEC Y TES": "Jardines del Nte., 97139 Mérida, Yuc.",
"CEDART ERMILO ABREU GÓMEZ": "Calle 21, Periférico Poniente, Colonia San Juan Bautista, 97200 Mérida, Yuc.",
"CEEAC": "C. 60 316-por 27 y 29, Señorial, 97059 Mérida, Yuc.",
"CEIC PLAYA DEL CARMEN": "Calle 22 Nte, Entre 50 y, Calle 55 Pte. &, Ejidal, 77712 Playa del Carmen, Q.R.",
"CELA": "Calle 21 No. 357A-x 26, San Pedro Cholul, 97138 Mérida, Yuc.",
"CENTRO EDUCATIVO MARIA GONZALEZ PALMA": "C. 50 454, Centro, 97000 Mérida, Yuc.",
"COREM MERIDA": "C. 26 Diag. 112, Las Brisas, 97144 Mérida, Yuc.",
"CENTENNIAL COLLEGIATE VOCATIONAL INSTITUTE": "289 College Ave W, Guelph, ON N1G 1S9, Canada",
"CENTRO ESCOLAR ROCHAVI": "C. 76 11-A'-1, Residencial Pensiones VI, 97217 Mérida, Yuc.",
"CESMAC": "C. 65 627, Parque Santiago, Centro, 97000 Centro, Yuc.",
"CETESC": "C. 61 496a-por 56 y 58, Centro, 97000 Mérida, Yuc.",
"CETIS 112": "C. 55 No. 728, Pacabtún, 97160 Mérida, Yuc.",
"CETIS 134": "Av. Lomas Verdes 2, Rancho Viejo, 91303 Banderilla, Ver.",
"CETIS 68": "Av. Aquiles Serdán 964, Tabachines, 81257 Los Mochis, Sin.",
"CENTRO DE ESTUDIOS TECNOLÓGICOS DEL MAR No 17": "Progreso, Boulevard Turístico Yucalpetén, 97320 Progreso, Yucatán",
"COLEGIO DE ESTUDIOS UNIVERSITARIOS DEL MAYAB": "C. 59 627, Barrio de Santiago, Centro, 97000 Mérida, Yuc.",
"COBAY CHOLUL": "97305 Mérida, Yucatán",
"CEMA": "Fracc, C. 27 150, San Miguel, 97140 Mérida, Yuc.",
"UNIVERSIDAD CNCI": "Calle 56 No. 508 Altos Centro, Mérida",
"COBAY CELESTUN": "C. 6 6480, Benito Juárez, 97367 Celestún, Yuc.",
"COLEGIO DE BACHILLERES DEL ESTADO DE CAMPECHE": "Calle Castillo Oliver No. 14, entre Lorenzo Alfaro Alomía y Avenida Miguel Alemán área Ah-Kim-Pech, C.P. 24014, San Francisco de Campeche, Campeche",
"COLEGIO DE BACHILLERES CHIAPAS": "Blvrd Presa Chicoasén 950, Amp las Palmas, 29044 Tuxtla Gutiérrez, Chis.",
"COLEGIO DE BACHILLERES QUINTANA ROO": "Calle 12 Entre Avenida 30, 77710 Playa del Carmen",
"COLEGIO BACHILLERES TABASCO": "Av. Paseo La Choca 100, Multiochenta, 86085 Villahermosa, Tab.",
"COLEGIO BACHILLERES DE TABASCO 46": "Villa las Flores, 86780 Jonuta, Tab.",
"COBATAB": "2000,, Av. Paseo La Choca 100, Parque Tabasco, 86035 Villahermosa, Tab.",
"COLEGIO DE BACHILLERES No. 8 TABASCO": "Av. Monte Cristo SN, Las Lomas, 86980 Emiliano Zapata, Tab.",
"COBAY PROGRESO": "C. 37 entre 72 y 74, Centro, 97320 Progreso, Yuc.",
"COBAY 5": "Carretera Federal Peto, Santa Rosa km 5, 97930 Peto, Yucatán",
"COBAY ACANCEH": "21 SN, Colonia las Palmas, Acanceh, Yucatán, México",
"COBAY BACA": "Calle 26 No. 107 Int. 0sn, Villa Baca, Baca, Yucatán",
"COBAY CAUCEL": "Hunucma - Caucel 56, Caucel, 97314 Caucel, Yuc.",
"COLEGIO DE BACHILLERES PLANTEL COZUMEL": "50 Avenida Sur, C. 27 Sur, San Miguel I, Cozumel, Q.R.",
"COBAY DZIDZANTUN": "Calle 23, entre 20 y 22 s/n. colonia Emiliano Zapata, Dzidzantún",
"COBAY HALACHO": "Calle 20, Colonia Salida, Halachó, Yucatán",
"COBAY KANASIN": "Calle 14 S/N x 33, 97370 Kanasín, Yucatán",
"COBAY KIMBILA": "Calle 13 0 S/N Kimbilá, Yuc.",
"COBAY KINCHIL": "Calle 18 SN, Kinchil, Yucatán",
"COLEGIO DE BACHILLERES DE YUCATAN": "Calle 34 No. 420 B x 35, Col. López Mateos, Mérida, Yucatán.",
"COBAY CHICXULUB PUEBLO": "Calle 12 x 15 y 17 carretera hacienda Guadalupe, 97340 Chicxulub, Yucatán",
"COBAY SANTA ROSA": "Av. 1o. de Mayo x 107 y 109, 97279 Mérida, Yucatán",
"COBAY TEKIT": "Calle 21 entre Calle 44, Tekit, Yucatán",
"COBAY TECOH": "Calle 28 Carretera Tecoh - Telchaquillo, Tecoh, Yucatán",
"COBAY TICUL": "C. 41 X 24 Y 24A Col. Santiago, 97370 Kanasín, Yucatán",
"COBAY UMAN": "Calle 16 S/n X 10 Y 12 Col. Cepeda Peraza, Umán, Yucatán",
"COBAY VALLADOLID": "Calle 32 S/N, Fernando Novelo, 97780 Valladolid, Yucatan",
"COBAY XOCLAN": "Calle 132 x 42, Xoclán Carmelitas, 97245 Mérida, Yucatán",
"PLANTEL COBAY SAN JOSE TZAL": "Calle 21, 97315 San José Tzal, Yucatán",
"COBAY TEABO": "Calle 23 57, 97910 Teabo, Yucatán",
"COBAY TIZIMIN": "Calle 48-B S/N por Calle 31, Centro, 97702 Tizimín, Yucatán",
"COLEGIO DE BACHILLERES PLANTEL JMM": "Av. Miguel Hidalgo Y Costilla S/N Colonia Guadalupe, C.P 78890, José María Morelos, Quintana Roo",
"COBAY SEYE": "Calle Sin Referencia, Pueblo Seyé, Yucatán, C.P. 97570.",
"COLEGIO MESOAMERICANO": "Calle 75, 542 A, Centro, Mérida, Yucatán",
"COLEGIO DEL GOLFO DE MERIDA": "Av. Itzaes No. 476-P Col. Centro, 97000 Mérida, Yucatán",
"COMPLUTENSE CENTRO INTEGRADO, INC. SAN LORENZO": "Mansiones de Monte Sereno, 22 C. 3, San Lorenzo, 00754, Puerto Rico",
"COLEGIO NACIONAL DE EDUCACIÓN PROFESIONAL TÉCNICA": "Calle 59 No. 729, Fraccionamiento Pacabtún, Mérida, Yucatán",
"CONALEP MERIDA": "Tablaje Catastral 31,800, Col. Polígono Chuburná, entre los km 38 y 39 del Periférico Poniente, Mérida, Yucatán",
"CONRADO MENENDEZ DIAZ": "Av Fidel Velázquez 849, 97169 Mérida, Yucatán",
"COBAY CUZAMA": "Km 2 carretera Cuzama Homun, Cuzamá, Yucatán",
"CENTRO UNIVERSITARIO FELIPE CARRILLO PUERTO": "Calle 65 583, 97000 Mérida, Yucatán",
"CUM": "Calle 5 x 18 S/n, 97133 Mérida, Yucatán",
"CENTRO UNIVERSITARIO MONTEJO": "Calle 60 No. 106 X 21 Y 23, 97205 Mérida, Yucatán ",
"COLEGIO YUCATAN": "Calle 26 #254 x 37, Limones, CP 97219, Mérida, Yucatán, México.",
"DAVID ALFARO SIQUEIROS MIRAFLORES": "Calle 15 230, Col. Miraflores, CP 97179, Mérida, Yucatán",
"EDUCACION INTEGRAL Y ACTIVA EDAI": "Av. Yucatán No. 524-1 x 22 y 24, Maya, 97134 Mérida, Yucatán, ",
"COLEGIO EDUCACION Y PATRIA": "Calle 64 x 57 y 59 No.485, Centro, 97000 Mérida, Yucatán",
"ELIGIO ANCONA": "Calle 59 No. 624, Barrio Santiago, Mérida, Yucatán",
"EMSAD 07 EL DESENGAÑO": "Carretera Justo Sierra-El Desengaño Candelaria, Campeche",
"ENEP UNAM SEP": "Av. Observatorio 170, Observatorio, Miguel Hidalgo, 11860 Ciudad de México, CDMX.",
"ESCUELA PREPARATORIA JOSE DOLORES RODRIGUEZ TAMAYO": "Calle 96 653 X 51A y 59, Ciudad Caucel, 97300 Mérida, Yucatán",
"PREPARATORIA ESTATAL NUM. 10": "Calle 59 Num. Ext. 821 Balcones Iii, Ciudad Caucel , Mérida, Yucatán",
"FRANCISCO DE MONTEJO Y LEON": "Calle 47 No. 514-A x 62 y 64 Col. Centro C.P. 97000, Mérida, Yucatán",
"FRANCISCO REPETO MILAN": "Calle 78 541, Col. Centro, CP 97000, Mérida, Yucatán",
"GONZALO CAMARA ZAVALA": "Calle 60 602, Col. Centro, CP 97000, Mérida, Yucatán",
"COBAY HUNUCMA": "Calle 26 No. Sn, Colonia Itzimna, Hunucmá, Yucatán",
"IBCEY": "Calle 31b #360 X 26 y 28, Col. Adolfo López Mateos, Mérida, Yucatán",
"INSTITUTO FELTON": "Calle 47-A #274 y 276 x 46 y 48 Fracc, Francisco de Montejo, 97203 Mérida, Yuc.",
"IMEI - CIUDAD DE MEXICO": "Calle 4 242, 08100 Ciudad de México, México",
"INCI - ALEMAN": "Calle 31-A 520, 97140 Mérida, Yucatán",
"INEVE": "S. Lorenzo 141, Tlacoquemecatl del Valle, Benito Juárez, 03200 Ciudad de México, México",
"INSTITUTO PATRIA": "Periférico Norte km. 2.5, San Ramón Nte, 97117 Mérida, Yucatán",
"INSTITUTO COMERCIAL BANCARIO": "Calle 62 No. 373, Colonia Centro, Mérida, Yucatán",
"INSTITUTO DAVID ALFARO": "Calle 65 230, 97179 Mérida, Yucatán ",
"INSTITUTO MEXICO": "Calle 50 290, Roma, 97218 Mérida, Yucatán",
"JOSE MARIA MORELOS Y PAVON": "Calle 15 Poniente 109, 97190 Mérida, Yucatán",
"JOSE VASCONCELOS": "Calle 59, 615E X 80 y 82, 97000 Mérida, Yucatán",
"JOSEFINA ROSADO DE PATRON": "Calle 67, NO. 437 entre Calle 40 y Calle 38, Mérida, Yucatán",
"PREPARATORIA JUVENTUS": "Calle 65 543.A, Parque Santiago, Centro, 97000 Mérida, Yucatán",
"COBAY KOMCHEN": "Calle 14 por 31, Komchen, 97300 Komchén, Yucatán",
"LUIS PASTEUR - CAMPECHE": "Gobernadores No. 295 Huanal, 24070 Campeche, Campeche",
"LA SALLE BOULLEWARES": "Colina de la Rumorosa no.70 Fracc. Boulevares, Naucalpan, Estado de México.",
"PREPARATORIA LAFAYETTE": "Calle 35 No. Sn, Colonia Cuauhtemoc, Ciudad Del Carmen, Carmen, Campeche C.P. 24170",
"LUIS ALVAREZ BARRET": "Calle 53 # 373, Entre 32 y 24. Chuminópolis, Chuminópolis, Mexico, 97158",
"MAHATMA GANDHI": "Calle 25B x 10 Colonia Lázaro Cárdenas 421, 97219 Mérida, Yucatán",
"CETMAR-PROGRESO": "C. 83 681F, 97320 Progreso, Yucatán",
"COLEGIO MANUEL SANCHEZ MARMOL": "Carlos Alberto Madrazo 90, 86800 Teapa, Tabasco",
"MANUEL CRESCENCIO REJON": "C. 69 452, 97000 Mérida, Yucatán",
"MEXICANA DEL MAYAB": "Calle 61 322, 97169 Mérida, Yucatán",
"PREPARATORIA MODELO": "Paseo de Montejo No.444, Centro, 97000 Mérida, Yucatán",
"PREPARATORIA MUNA": "Calle 19, colonia Ninguno, municipio Muna, Yucatán, C.P. 97840",
"UNIVERSIDAD DE MUNDO MAYA": "Calle 51 por 50 y 48 #472 Col. Centro, C.P.97000, Mérida, Yucatán",
"COBAY PLANTEL PETO": "Carretera Federal Peto, Santa Rosa km 5, 97930 Peto, Yucatán",
"PREPARATORIA 7": "Calle 12, 97149 Mérida, Yucatán",
"PREPA ACANCEH": "Acanceh, 97380 112 Calle 25, 97380 Acanceh, Yucatán",
"PREPA ABIERTA": "Calle 31-A por 8, Col. San Esteban, C. P. 97149, Mérida, Yucatán",
"PREPARATORIA LIBRE": "Calle Benito Juárez, Av. Soledad 707, 78430 Soledad de Graciano Sánchez, S.L.P.",
"PREPA LIBRE SEP": "N/A",
"PREPARATORIA ESTATAL No. 8": "C. 51, Francisco de Montejo II X 58 y 60, 97203 Mérida, Yucatán",
"PREPARATORIA ESTATAL CTM #3": "Calle 57A 744, 97160 Mérida",
"PREPA 1": "en CIL-UADY, Calle 41 entre 14, 97150 Mérida, Yucatán",
"PREPARATORIA 11": "Calle 59-C LOTE 950, 97000 Mérida, Yucatán",
"PREPARATORIA ESTATAL 3": "Calle 57A 744, 97160 Mérida",
"PREPA 4 CANSAHCAB": "Calle 20 S/N, Cansahcab Centro, 97410 Cansahcab, Yucatán",
"PREPARATORIA #5 AGUSTIN FRANCO VILLANUEVA": "Calle 67 por 50, 97000 Mérida, Yucatán",
"PREPA 7": "Calle 12, 97149 Mérida, Yucatán",
"PREPARATORIA NO. 8": "C. 51, Francisco de Montejo II X 58 y 60, 97203 Mérida, Yucatán",
"VICTOR MANUEL CERVERA PACHECO": "C. 12-D 2a, 97370 Kanasín, Yucatán",
"PREPARATORIA ESTATAL 2": "Calle 20 Pedregales De Tanlum Mérida, Yucatán CP. 97210",
"PREPARATORIA MEXICO": "C. 72 453, 97000 Mérida, Yucatán",
"PREPARATORIA MIGUEL ANGEL": "Calle 5 Sur N, 97139 Mérida, Yucatán",
"PREPARATORIA PROGRESO": "C. 44 145-7, 97320 Progreso, Yucatán",
"PREPARATORIA DE TAHDZIBICHEN": "Calle Ninguno 0, Colonia Ninguno, Yaxcabá, Yucatán. Cp. 97927",
"PREPARATORIA YUCATAN": "Calle 61 # 551 x 70 y 72, Col. Centro, CP. 97000 Mérida, Yucatán",
"PREPARATORIA 1 UADY": "en CIL-UADY, Calle 41 entre 14, 97150 Mérida, Yucatán",
"PREPARATORIA 3 UADY": "Calle 185 sin número X 90-B y 92 San Luis Sur y Avenida 86 Mérida, Yucatán",
"PREPARATORIA 4": "En Calle 20 S/N, Colonia Ninguno, Cansahcab, Yucatán",
"PREPARATORIA ESTATAL No. 9": "YUC 31, 97880 Oxkutzcab, Yucatán",
"PRONACE": "Calle 62 #685 x 45 y 43, Fracc. Pedregales, C.P. 97300, Cd. Caucel",
"REPUBLICA DE MEXICO": "Calle 72 Av. Reforma #453 x 51 y 53, Centro, CP 97000, Mérida, Yucatán",
"RICARDO FLORES MAGÓN": "Calle 21 102B x 20 y 22, 97400 Telchac, Yucatán",
"ROGERS HALL": "Calle 21 No. 131 x 32 y 36 Col. Buenavista, Mérida, Yucatán",
"SERAPIO RENDÓN": "Calle 46-b Serapio Rendon, Mérida, Yucatán CP. 97285",
"SALVADOR ALVARADO": "Cll 20 302, 97205 Mérida, Yucatán",
"COLEGIO SAN AGUSTIN": "C. 58 480B, 97000 Mérida, Yucatán",
"SIGLO XXI": "Calle 21 216, Mérida, Yucatán",
"SERVICIO NACIONAL DE BACHILLERATO EN LINEA": "N/A",
"COBAY TEKAX": "Calle 55 s/n x 78 y 84 Fraccionamiento Vivah, 97970 Tekax, Yucatán",
"UNIVERSIDAD TECMILENIO": "Calle 53 Diagonal S/N, 97302 Mérida, Yucatán",
"TELEBACHILLERATO": "C. 22 148, 97348 Yaxkukul, Yucatán",
"JOSE DOLORES RODRIGUEZ TICUL": "Calle 18 No. 175, 97860 Ticul, Yucatán",
"COBAY TIXPEUAL": "C. 25 entre 17 y 19, 97386 Tixpéhual, Yucatán",
"UNACAR - CAMPUS II": "Av Concordia, 24180 Carmen, Campeche",
"UABIC": "Calle 185 20, 97315 Mérida, Yucatán",
"PREPARATORIA 2 UADY": "Calle 59C 204, 97238 Mérida, Yucatán",
"SAN AGUSTIN": "C. 58 480B, 97000 Mérida, Yucatán",
"UNIVERSIDAD MEXICO AMERICANA DEL NORTE A.C.": "Primera s/n, Col. Círculo, CP 88640, Reynosa, Tamaulipas, México",
"UPAV VERACRUZ": "CALLE GUILLERMO PRIETO 8, XALAPA VERACRUZ DE IGNACIO DE LA LLAVE",
"UPP PREPA": "Av Jacinto Canek 739, Paseo de las Fuentes, 97230 Mérida, Yucatán",
"UVM": "Calle 79 500, Dzityá Polígono, 97302 Mérida, Yucatán",
"ESCUELA NACIONAL PREPARATORIA 4 VIDAL CASTAÑEDA Y": "Av Observatorio 170-P. B, Observatorio, Miguel Hidalgo, 11860 Ciudad de México",
}

os.makedirs("csv_vizcaya", exist_ok=True)

# =========================
# FUNCIONES
# =========================

CLAVES_CARRERA = {
    "Arquitectura": {
        "Escolarizada": "01",
        "Mixto/Sabatino": "20"
    },

    "Educación": {
        "Escolarizada": "02",
        "Mixto/Sabatino": "31"
    },

    "Contabilidad": {
        "Escolarizada": "12",
        "Mixto/Sabatino": "32"
    },

    "Criminología": {
        "Escolarizada": "16"
    },

    "Derecho": {
        "Escolarizada": "08",
        "Mixto/Sabatino": "35"
    },

    "Diseño de Modas": {
        "Escolarizada": "06",
        "Mixto/Sabatino": "33"
    },

    "Enfermería": {
        "Escolarizada": "09"
    },

    "Fisioterapia": {
        "Escolarizada": "10"
    },

    "Gastronomía": {
        "Escolarizada": "04",
        "Mixto/Sabatino": "36"
    },

    "Ingeniería Civil": {
        "Mixto/Sabatino": "37"
    },

    "Nutrición": {
        "Escolarizada": "13",
        "Mixto/Sabatino": "25"
    },

    "Psicología": {
        "Escolarizada": "15",
        "Mixto/Sabatino": "28"
    },

    "Administración de Empresas": {
        "Escolarizada": "14",
        "Mixto/Sabatino": "27"
    },

    "Odontología": {
        "Escolarizada": "17"
    }
}

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


def matricula_sucia(anio, clave_carrera):
    anio_2_digitos = str(anio)[-2:]          # 2018 -> 18
    ultimos_dos = random.randint(1, 50)      # 01 - 50
    rrr = f"0{ultimos_dos:02d}"               # 001 - 050
    return f"{anio_2_digitos}{clave_carrera}{rrr}"

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
            "modalidad",
            "ubicacion_escuela_procedencia",
            "nivel",
            "carrera",
            "turno",
            "ciclo"
        ])

        for _ in range(total):

            # ---------- CARRERA + CICLO ----------
            if random.random() < 0.5:
                carrera = random.choice(CARRERAS_CUATRI)
                ciclo = random.choice(CICLO_CUATRIMESTRAL)
            else:
                carrera = random.choice(CARRERA_SEMESTRE)
                ciclo = random.choice(CICLO_SEMESTRAL)

            # ---------- MODALIDAD Y CLAVE ----------
            modalidad = random.choice(list(CLAVES_CARRERA[carrera].keys()))
            clave_carrera = CLAVES_CARRERA[carrera][modalidad]

            # ---------- ESCUELA ----------
            escuela = random.choice(ESCUELAS)
            ubicacion_escuela = UBICACIONES_ESCUELA[escuela]
            
            writer.writerow([
                matricula_sucia(anio, clave_carrera),
                random.choice(SEXO_SUCIO),
                random.choice(NACIONALIDAD_SUCIA),
                random.choice([
                    "Yucatán",
                    "Campeche",
                    "Quintana Roo",
                    "Baja California", 
                    "Canada", 
                    "Chihuahua", 
                    "Veracruz", 
                    "Sinaloa", 
                    "Monterrey", 
                    "Chiapas", 
                    "Tabasco", 
                    "San Lorenzo", 
                    "Ciudad de Mexico", 
                    "Puebla", 
                    "Tamaulipas", 
                    "Aguascalientes", 
                    "Michoacán"]),
                fecha_nacimiento_sucia(),
                random.choice(TIPO_INGRESO),
                random.choice(COLONIAS),
                escuela,
                modalidad,
                ubicacion_escuela,
                random.choice(NIVELES),
                carrera,
                random.choice(TURNOS),
                ciclo
            ])

    print(f"CSV generado: {filename}")
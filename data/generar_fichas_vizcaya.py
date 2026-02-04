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
    "Ing. Civil",
    "Ing. en Procesos de Manufactura",
    "Lic. en Admin. de Empresas",
    "Lic. en Arquitectura",
    "Lic. en Contabilidad",
    "Lic. en Criminología",
    "Lic. en Derecho",
    "Lic. en Diseño de Modas",
    "Lic. en Enfermería",
    "Lic. en Educación",
    "Lic. en Fisioterapia",
    "Lic. en Gastronomía",
    "Lic. en Nutrición",
    "Lic. en Psicología"
]

CARRERA_SEMESTRE = [
    "Lic. en Odontología", 
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
    "COBACAM-CAMPECHE",
    "COLEGIO DE BACHILLERES CHIAPAS",
    "COBACH CHIAPAS",
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

UBICACIONES_ESCUELA = [
    "Calle 19 91, Ciudad Ninguno, Cacalchén, Yucatán. Cp. 97460", # COBAY CACALCHEN
    "Calle 59, s/n 102-A y 106, Cd Caucel, 97314 Mérida, Yuc.", # PREPARATORIA ESTATAL #10 RUBÉN H. RODRÍGUEZ MOGUEL
    "Calle 33 #140 Entre calle 20 A y 22 Col, Chuburná de Hidalgo, 97205 Mérida, Yuc.", # UNIVERSIDAD VIZCAYA DE LAS AMÉRICAS
    "NA", # ACUERDO 286
    "Calle 24 No 318 y 320, San Pedro Cholul, 97138 Mérida, Yuc.", # ALIANZ COMUNIDAD ESTUDIANTIL
    "C. 64 602, entre 75, 97000 Mérida, Yucatán", # ALIANZA DE CAMIONEROS
    "Calle 23 s/n x 44a y 44b CCT 31EBH0004B, Mérida, Mexico, 97219", # PLANTEL AZTECA
    "NA", # BACHILLERATO EN LINEA UADY
    "Boulevard Benito Juárez 1404, Monclova, Coahuila de Zaragoza.", # BACHILLERES AMERICAS
    "Calle 25 S/N, Brisas del Pasaje, 97144 Mérida, Yuc.", # BETANCOURT - BRISAS
    "97115 Mérida, Yucatán·", # FELIPE ESCALANTE RUZ BRISAS Calle 24
    "97810 Samahil, Yuc.", # BACHILLERATO COMUNITARIO SAMAHIL
    "Calle 4, 21 Y 25, C. 4 SN, Centro, 97620 Buctzotz, Yucatán", # COBAY BUCTOZTZ
    "97470 Tixkokob, Yucatán", # COBAY TIXKOKOB
    "Av. Chichen-Itza Supermanzana 1, 77500 Cancún, Q.R.", # CBTIS 111 CANCUN
    "C. 13 101 por 60, 97205 Mérida, Yucatán", # CBETIS 120
    "24902, Calle 22-A 4100, Fátima, 24902 Calkiní, Camp.", # CBTIS 126 CAMPECHE
    "Calle 27 369, Edesio Carrillo Puerto, 97430 Motul de Carrillo, 97430", # CBTIS 80
    "C. 72 499, Barrio de Santiago, Centro, 97000 Mérida, Yuc.", # COLEGIO AMERICANO
    "50 Avenida Sur, C. 27 Sur, San Miguel I, 77666 Cozumel, Q.R.", # COBACH COZUMEL
    "Calle 32, Por Calle 25 y 27 SN, Residencial del Nte, 97219 Mérida, Yuc.", # COBAY CHENKU
    "97580 Homún, Yucatán", # COBAY HOMUN
    "Calle 20 x 11 carretera a Tibolón, 40 X 11, 97690 Sotuta, Yucatán", # COBAY SOTUTA
    "C. 30, 97960 Tzucacab, Yuc.", # COBAY TZUCACAB
    "Ex-Hacienda Xmatkuil A.P. 970 Xmatkuil, 97139 Mérida, Yuc.", # CBTA 13 XMATKUIL
    "C. 22, 97920 Yaxcabá, Yuc.", # COBAY YAXCABA
    "Unnamed Road, 97825 Abalá, Yuc.", # COBAY ABALA
    "CALLE DEL BARRO, Av. Poblado Islas Agrarias # 1201, 21600 Mexicali, B.C.", # PREPARATORIA ABIERTA CALAFIA
    "Calle 20 S/N, Cansahcab Centro, 97410 Cansahcab, Yuc.", # VICTOR J. MANZANILLA J. - CANSAHCAB
    "Antonio González Fernández. 600, 10 de Abril, 77622 Cozumel, Q.R.", # CBTIS 28 COZUMEL
    "C. 107, Santa Rosa, 97279 Mérida, Yuc.", # COLEGIO BENITO JUAREZ GARCIA
    "97315 Mérida, Yucatán", # CENTRO DE BACHILLERATO TECNOLOGICO AGROPECUARIO
    "C. 30 102, Guadalupe, 97540 Izamal, Yuc.", # CBTA 165
    "C. 30 102, Guadalupe, 97540 Izamal, Yuc.", # CBTA IZAMAL 185
    "Calle 18 No. 300-X 49, Salvador Alvarado Sur, 97190 Mérida, Yuc.", # CBTIS 95
    "C. 13 101 por 60, Loma Bonita, 97205 Mérida, Yuc.", # CBTIS 120 MÉRIDA
    "Calle 51, Francisco de Montejo, Mérida, Yucatán", # CARLOS CASTILLO PERAZA 
    "C. 56 4, Benito Juárez, 24180 Cdad. del Carmen, Camp.", # UNIVERSIDAD AUTÓNOMA DEL CARMEN
    "C. 21 216, entre 60 Y 62, Zona Dorada II, 97226 Mérida, Yuc.", # CENTRO EDUCATIVO SIGLO XXI
    "Cl. 143 314, Emiliano Zapata Sur L, 97297 Mérida, Yuc.", # CECYTE
    "C. 4 Pte. s/n, Maya Pax, Mayapax, 77780 Tulum, Q.R.", # CECYTE QUINTANA ROO
    "Jardines del Nte., 97139 Mérida, Yuc.", # CEC Y TES
    "Calle 21, Periférico Poniente, Colonia San Juan Bautista, 97200 Mérida, Yuc.", # CEDART ERMILO ABREU GÓMEZ
    "C. 60 316-por 27 y 29, Señorial, 97059 Mérida, Yuc.", # CEEAC
    "Calle 22 Nte, Entre 50 y, Calle 55 Pte. &, Ejidal, 77712 Playa del Carmen, Q.R.", # CEIC PLAYA DEL CARMEN
    "Calle 21 No. 357A-x 26, San Pedro Cholul, 97138 Mérida, Yuc.", # CELA
    "C. 50 454, Centro, 97000 Mérida, Yuc.", # CENTRO EDUCATIVO MARIA GONZALEZ PALMA
    "C. 26 Diag. 112, Las Brisas, 97144 Mérida, Yuc.", # COREM MERIDA
    "289 College Ave W, Guelph, ON N1G 1S9, Canada", # CENTENNIAL COLLEGIATE VOCATIONAL INSTITUTE
    "C. 76 11-A'-1, Residencial Pensiones VI, 97217 Mérida, Yuc.", # CENTRO ESCOLAR ROCHAVI
    "C. 65 627, Parque Santiago, Centro, 97000 Centro, Yuc.", # CESMAC
    "C. 61 496a-por 56 y 58, Centro, 97000 Mérida, Yuc.", # CETESC
    "C. 55 No. 728, Pacabtún, 97160 Mérida, Yuc.", # CETIS 112
    "Av. Lomas Verdes 2, Rancho Viejo, 91303 Banderilla, Ver.", # CETIS 134
    "Av. Aquiles Serdán 964, Tabachines, 81257 Los Mochis, Sin.", # CETIS 68
    "Progreso, Boulevard Turístico Yucalpetén, 97320 Progreso, Yucatán", # CENTRO DE ESTUDIOS TECNOLÓGICOS DEL MAR No 17
    "C. 59 627, Barrio de Santiago, Centro, 97000 Mérida, Yuc.", # COLEGIO DE ESTUDIOS UNIVERSITARIOS DEL MAYAB
    "97305 Mérida, Yucatán", # COBAY CHOLUL
    "Fracc, C. 27 150, San Miguel, 97140 Mérida, Yuc.", # CEMA
    "Calle 56 No. 508 Altos Centro, Mérida", # UNIVERSIDAD CNCI
    "C. 6 6480, Benito Juárez, 97367 Celestún, Yuc.", # COBAY CELESTUN
    "Calle Castillo Oliver No. 14, entre Lorenzo Alfaro Alomía y Avenida Miguel Alemán área Ah-Kim-Pech, C.P. 24014, San Francisco de Campeche, Campeche", # COLEGIO DE BACHILLERES DEL ESTADO DE CAMPECHE
    "Blvrd Presa Chicoasén 950, Amp las Palmas, 29044 Tuxtla Gutiérrez, Chis.", # COLEGIO DE BACHILLERES CHIAPAS
    "Blvrd Presa Chicoasén 950, Amp las Palmas, 29044 Tuxtla Gutiérrez, Chis.", # COBACH CHIAPAS
    "Calle 12 Entre Avenida 30, 77710 Playa del Carmen", # COLEGIO DE BACHILLERES QUINTANA ROO
    "Av. Paseo La Choca 100, Multiochenta, 86085 Villahermosa, Tab.", # COLEGIO BACHILLERES TABASCO
    "Villa las Flores, 86780 Jonuta, Tab.", # COLEGIO BACHILLERES DE TABASCO 46
    "2000,, Av. Paseo La Choca 100, Parque Tabasco, 86035 Villahermosa, Tab.", # COBATAB
    "Av. Monte Cristo SN, Las Lomas, 86980 Emiliano Zapata, Tab.", # COLEGIO DE BACHILLERES No. 8 TABASCO
    "C. 37 entre 72 y 74, Centro, 97320 Progreso, Yuc.", # COBAY PROGRESO
    "Carretera Federal Peto, Santa Rosa km 5, 97930 Peto, Yucatán", # COBAY 5
    "21 SN, Colonia las Palmas, Acanceh, Yucatán, México", # COBAY ACANCEH
    "Calle 26 No. 107 Int. 0sn, Villa Baca, Baca, Yucatán", # COBAY BACA
    "Hunucma - Caucel 56, Caucel, 97314 Caucel, Yuc.", # COBAY CAUCEL
    "50 Avenida Sur, C. 27 Sur, San Miguel I, Cozumel, Q.R.", # COLEGIO DE BACHILLERES PLANTEL COZUMEL
    "Calle 23, entre 20 y 22 s/n. colonia Emiliano Zapata, Dzidzantún", # COBAY DZIDZANTUN
    "Calle 20, Colonia Salida, Halachó, Yucatán", # COBAY HALACHO
    "Calle 14 S/N x 33, 97370 Kanasín, Yucatán", # COBAY KANASIN
    "Calle 13 0 S/N Kimbilá, Yuc.", # COBAY KIMBILA
    "Calle 18 SN, Kinchil, Yucatán", # COBAY KINCHIL
    "Calle 34 No. 420 B x 35, Col. López Mateos, Mérida, Yucatán.", # COLEGIO DE BACHILLERES DE YUCATAN
    "Calle 12 x 15 y 17 carretera hacienda Guadalupe, 97340 Chicxulub, Yucatán", # COBAY CHICXULUB PUEBLO
    "Av. 1o. de Mayo x 107 y 109, 97279 Mérida, Yucatán", # COBAY SANTA ROSA
    "Calle 21 entre Calle 44, Tekit, Yucatán", # COBAY TEKIT
    "Calle 28 Carretera Tecoh - Telchaquillo, Tecoh, Yucatán", # COBAY TECOH
    "Calle 41 x 24 y 24A Col. Santiago, Ticul, Yucatán.", # COBAY TICUL
    "Calle 16 S/n X 10 Y 12 Col. Cepeda Peraza, Umán, Yucatán", # COBAY UMAN
    "Calle 32 S/N, Fernando Novelo, 97780 Valladolid, Yucatan", # COBAY VALLADOLID
    "Calle 132 x 42, Xoclán Carmelitas, 97245 Mérida, Yucatán", # COBAY XOCLAN
    "Calle 21, 97315 San José Tzal, Yucatán", # PLANTEL COBAY SAN JOSE TZAL
    "Calle 23 57, 97910 Teabo, Yucatán", # COBAY TEABO
    "Calle 48-B S/N por Calle 31, Centro, 97702 Tizimín, Yucatán", # COBAY TIZIMIN
    "Av. Miguel Hidalgo Y Costilla S/N Colonia Guadalupe, C.P 78890, José María Morelos, Quintana Roo", # COLEGIO DE BACHILLERES PLANTEL JMM
    "Calle Sin Referencia, Pueblo Seyé, Yucatán, C.P. 97570.", # COBAY SEYE
    "Calle 75, 542 A, Centro, Mérida, Yucatán", # COLEGIO MESOAMERICANO
    "Av. Itzaes No. 476-P Col. Centro, 97000 Mérida, Yucatán", # COLEGIO DEL GOLFO DE MERIDA
    "Mansiones de Monte Sereno, 22 C. 3, San Lorenzo, 00754, Puerto Rico", # COMPLUTENSE CENTRO INTEGRADO, INC. SAN LORENZO
    "Calle 59 No. 729, Fraccionamiento Pacabtún, Mérida, Yucatán", # COLEGIO NACIONAL DE EDUCACIÓN PROFESIONAL TÉCNICA
    "Tablaje Catastral 31,800, Col. Polígono Chuburná, entre los km 38 y 39 del Periférico Poniente, Mérida, Yucatán", # CONALEP MERIDA
    "Av Fidel Velázquez 849, 97169 Mérida, Yucatán", # CONRADO MENENDEZ DIAZ
    "Km 2 carretera Cuzama Homun, Cuzamá, Yucatán", # COBAY CUZAMA
    "Calle 65 583, 97000 Mérida, Yucatán", # CENTRO UNIVERSITARIO FELIPE CARRILLO PUERTO
    "Calle 5 x 18 S/n, 97133 Mérida, Yucatán", # CUM
    "Calle 60 No. 106 X 21 Y 23, 97205 Mérida, Yucatán ", # CENTRO UNIVERSITARIO MONTEJO
    "Calle 26 #254 x 37, Limones, CP 97219, Mérida, Yucatán, México.", # COLEGIO YUCATAN
    "Calle 15 230, Col. Miraflores, CP 97179, Mérida, Yucatán", # DAVID ALFARO SIQUEIROS MIRAFLORES
    "Av. Yucatán No. 524-1 x 22 y 24, Maya, 97134 Mérida, Yucatán, ", # EDUCACION INTEGRAL Y ACTIVA EDAI
    "Calle 64 x 57 y 59 No.485, Centro, 97000 Mérida, Yucatán", # COLEGIO EDUCACION Y PATRIA
    "Calle 59 No. 624, Barrio Santiago, Mérida, Yucatán", # ELIGIO ANCONA
    "Carretera Justo Sierra-El Desengaño Candelaria, Campeche", # EMSAD 07 EL DESENGAÑO
    "Av. Observatorio 170, Observatorio, Miguel Hidalgo, 11860 Ciudad de México, CDMX.", # ENEP UNAM SEP
    "Calle 96 653 X 51A y 59, Ciudad Caucel, 97300 Mérida, Yucatán", # ESCUELA PREPARATORIA JOSE DOLORES RODRIGUEZ TAMAYO
    "Calle 59 Num. Ext. 821 Balcones Iii, Ciudad Caucel , Mérida, Yucatán", # PREPARATORIA ESTATAL NUM. 10
    "Calle 47 No. 514-A x 62 y 64 Col. Centro C.P. 97000, Mérida, Yucatán", # FRANCISCO DE MONTEJO Y LEON
    "Calle 78 541, Col. Centro, CP 97000, Mérida, Yucatán", # FRANCISCO REPETO MILAN
    "Calle 60 602, Col. Centro, CP 97000, Mérida, Yucatán", # GONZALO CAMARA ZAVALA
    "Calle 26 No. Sn, Colonia Itzimna, Hunucmá, Yucatán", # COBAY HUNUCMA
    "Calle 31b #360 X 26 y 28, Col. Adolfo López Mateos, Mérida, Yucatán", # IBCEY
    "Calle 47-A #274 y 276 x 46 y 48 Fracc, Francisco de Montejo, 97203 Mérida, Yuc.", # INSTITUTO FELTON
    "Calle 4 242, 08100 Ciudad de México, México", # IMEI - CIUDAD DE MEXICO
    "Calle 31-A 520, 97140 Mérida, Yucatán", # INCI - ALEMAN
    "S. Lorenzo 141, Tlacoquemecatl del Valle, Benito Juárez, 03200 Ciudad de México, México", # INEVE
    "Periférico Norte km. 2.5, San Ramón Nte, 97117 Mérida, Yucatán", # INSTITUTO PATRIA
    "Calle 62 No. 373, Colonia Centro, Mérida, Yucatán", # INSTITUTO COMERCIAL BANCARIO
    "Calle 65 230, 97179 Mérida, Yucatán ", # INSTITUTO DAVID ALFARO
    "Calle 50 290, Roma, 97218 Mérida, Yucatán", # INSTITUTO MEXICO
    "Calle 15 Poniente 109, 97190 Mérida, Yucatán", # JOSE MARIA MORELOS Y PAVON
    "Calle 59, 615E X 80 y 82, 97000 Mérida, Yucatán", # JOSE VASCONCELOS
    "Calle 67, NO. 437 entre Calle 40 y Calle 38, Mérida, Yucatán", # JOSEFINA ROSADO DE PATRON
    "Calle 65 543.A, Parque Santiago, Centro, 97000 Mérida, Yucatán", # PREPARATORIA JUVENTUS
    "Calle 14 por 31, Komchen, 97300 Komchén, Yucatán", # COBAY KOMCHEN
    "Gobernadores No. 295 Huanal, 24070 Campeche, Campeche", # LUIS PASTEUR - CAMPECHE
    "Colina de la Rumorosa no.70 Fracc. Boulevares, Naucalpan, Estado de México.", # LA SALLE BOULEVARES
    "Calle 35 No. Sn, Colonia Cuauhtemoc, Ciudad Del Carmen, Carmen, Campeche C.P. 24170",  # PREPARATORIA LAFAYETTE
    "Calle 53 # 373, Entre 32 y 24. Chuminópolis, Chuminópolis, Mexico, 97158", # LUIS ALVAREZ BARRET
    "Calle 25B x 10 Colonia Lázaro Cárdenas 421, 97219 Mérida, Yucatán", # MAHATMA GANDHI
    "C. 83 681F, 97320 Progreso, Yucatán", # CETMAR-PROGRESO
    "Carlos Alberto Madrazo 90, 86800 Teapa, Tabasco", # COLEGIO MANUEL SANCHEZ MARMOL
    "C. 69 452, 97000 Mérida, Yucatán", # MANUEL CRESCENCIO REJON
    "Calle 61 322, 97169 Mérida, Yucatán", # MEXICANA DEL MAYAB
    "Paseo de Montejo No.444, Centro, 97000 Mérida, Yucatán", # PREPARATORIA MODELO
    "Calle 19, colonia Ninguno, municipio Muna, Yucatán, C.P. 97840", # PREPARATORIA MUNA
    "Calle 51 por 50 y 48 #472 Col. Centro, C.P.97000, Mérida, Yucatán", # UNIVERSIDAD DE MUNDO MAYA
    "Carretera Federal Peto, Santa Rosa km 5, 97930 Peto, Yucatán", # COBAY PLANTEL PETO
    "Calle 12, 97149 Mérida, Yucatán", # PREPARATORIA 7
    "Acanceh, 97380 112 Calle 25, 97380 Acanceh, Yucatán", # PREPA ACANCEH
    "Calle 31-A por 8, Col. San Esteban, C. P. 97149, Mérida, Yucatán", # PREPA ABIERTA
    "Calle Benito Juárez, Av. Soledad 707, 78430 Soledad de Graciano Sánchez, S.L.P.",  # PREPARATORIA LIBRE
    "N/A", # PREPA LIBRE SEP
    "C. 51, Francisco de Montejo II X 58 y 60, 97203 Mérida, Yucatán", # PREPARATORIA ESTATAL No. 8
    "Calle 57A 744, 97160 Mérida", # PREPARATORIA ESTATAL CTM #3
    "en CIL-UADY, Calle 41 entre 14, 97150 Mérida, Yucatán", # PREPA 1
    "Calle 59-C LOTE 950, 97000 Mérida, Yucatán", # PREPARATORIA 11
    "Calle 57A 744, 97160 Mérida", # PREPARATORIA ESTATAL 3
    "Calle 20 S/N, Cansahcab Centro, 97410 Cansahcab, Yucatán", # PREPA 4 CANSAHCAB
    "Calle 67 por 50, 97000 Mérida, Yucatán", # PREPARATORIA #5 AGUSTIN FRANCO VILLANUEVA
    "Calle 12, 97149 Mérida, Yucatán", # PREPA 7
    "C. 51, Francisco de Montejo II X 58 y 60, 97203 Mérida, Yucatán", # PREPARATORIA NO. 8
    "C. 12-D 2a, 97370 Kanasín, Yucatán", # VICTOR MANUEL CERVERA PACHECO
    "Calle 20 Pedregales De Tanlum Mérida, Yucatán CP. 97210", # PREPARATORIA ESTATAL 2
    "C. 72 453, 97000 Mérida, Yucatán", # PREPARATORIA MEXICO
    "Calle 5 Sur N, 97139 Mérida, Yucatán", # PREPARATORIA MIGUEL ANGEL
    "C. 44 145-7, 97320 Progreso, Yucatán", # PREPARATORIA PROGRESO
    "Calle Ninguno 0, Colonia Ninguno, Yaxcabá, Yucatán. Cp. 97927", # PREPARATORIA DE TAHDZIBICHEN
    "Calle 61 # 551 x 70 y 72, Col. Centro, CP. 97000 Mérida, Yucatán", # PREPARATORIA YUCATAN
    "en CIL-UADY, Calle 41 entre 14, 97150 Mérida, Yucatán", # PREPARATORIA 1 UADY
    "Calle 185 sin número X 90-B y 92 San Luis Sur y Avenida 86 Mérida, Yucatán", # PREPARATORIA 3 UADY
    "En Calle 20 S/N, Colonia Ninguno, Cansahcab, Yucatán", # PREPARATORIA 4
    "YUC 31, 97880 Oxkutzcab, Yucatán",  # PREPARATORIA ESTATAL No. 9
    "Calle 62 #685 x 45 y 43, Fracc. Pedregales, C.P. 97300, Cd. Caucel",  # PRONACE
    "Calle 72 Av. Reforma #453 x 51 y 53, Centro, CP 97000, Mérida, Yucatán", # REPUBLICA DE MEXICO
    "Calle 21 102B x 20 y 22, 97400 Telchac, Yucatán", # RICARDO FLORES MAGÓN
    "Calle 21 No. 131 x 32 y 36 Col. Buenavista, Mérida, Yucatán", # ROGERS HALL
    "Calle 46-b Serapio Rendon, Mérida, Yucatán CP. 97285", # SERAPIO RENDÓN
    "Cll 20 302, 97205 Mérida, Yucatán", # SALVADOR ALVARADO
    "C. 58 480B, 97000 Mérida, Yucatán", # COLEGIO SAN AGUSTIN
    "Calle 21 216, Mérida, Yucatán", # SIGLO XXI
    "N/A", # SERVICIO NACIONAL DE BACHILLERATO EN LINEA
    "Calle 55 s/n x 78 y 84 Fraccionamiento Vivah, 97970 Tekax, Yucatán", # COBAY TEKAX
    "Calle 53 Diagonal S/N, 97302 Mérida, Yucatán", # UNIVERSIDAD TECMILENIO
    "C. 22 148, 97348 Yaxkukul, Yucatán", # TELEBACHILLERATO
    "C. 41 X 24 Y 24A Col. Santiago, 97370 Kanasín, Yucatán", # COBAY TICUL
    "Calle 18 No. 175, 97860 Ticul, Yucatán", # JOSE DOLORES RODRIGUEZ TICUL
    "C. 25 entre 17 y 19, 97386 Tixpéhual, Yucatán", # COBAY TIXPEUAL
    "Av Concordia, 24180 Carmen, Campeche", # UNACAR - CAMPUS II
    "Calle 185 20, 97315 Mérida, Yucatán", # UABIC
    "Calle 59C 204, 97238 Mérida, Yucatán", # PREPARATORIA 2 UADY
    "C. 58 480B, 97000 Mérida, Yucatán", # SAN AGUSTIN
    "Primera s/n, Col. Círculo, CP 88640, Reynosa, Tamaulipas, México", # UNIVERSIDAD MEXICO AMERICANA DEL NORTE A.C.
    "CALLE GUILLERMO PRIETO 8, XALAPA VERACRUZ DE IGNACIO DE LA LLAVE", # UPAV VERACRUZ
    "Av Jacinto Canek 739, Paseo de las Fuentes, 97230 Mérida, Yucatán", # UPP PREPA
    "Calle 79 500, Dzityá Polígono, 97302 Mérida, Yucatán", # UVM
    "Av Observatorio 170-P. B, Observatorio, Miguel Hidalgo, 11860 Ciudad de México", # ESCUELA NACIONAL PREPARATORIA 4 VIDAL CASTAÑEDA Y
]

os.makedirs("csv_vizcaya", exist_ok=True)

# =========================
# FUNCIONES
# =========================

CLAVES_CARRERA = {
    "Arquitectura": {
        "Escolarizada": "01",
        "Mixto/Sabatino": "20"
    },

    "Ciencias de la Educación": {
        "Escolarizada": "02",
        "Mixto/Sabatino": "31"
    },

    "Contaduría Pública": {
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
            ubicacion_escuela = UBICACIONES_ESCUELA.get(escuela, "")

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
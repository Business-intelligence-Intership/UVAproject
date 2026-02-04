import csv
import re

INPUT_CSV = "escuelas.csv"
OUTPUT_TXT = "lista_formateada.txt"


def limpiar_direccion(s: str) -> str:
    if not s:
        return ""

    s = str(s).strip()

    # arreglar comillas rotas
    s = s.replace('""', '"')
    s = s.replace('"', "")

    # quitar Mexico
    s = re.sub(r",?\s*Mexico\.?$", "", s, flags=re.IGNORECASE).strip()

    # normalizaciones
    s = re.sub(r"\bMerida\b", "Mérida", s, flags=re.IGNORECASE)
    s = re.sub(r"\bYucatan\b", "Yucatán", s, flags=re.IGNORECASE)

    # limpiar dobles espacios
    s = re.sub(r"\s+", " ", s).strip()

    # quitar coma final
    s = re.sub(r",\s*$", "", s).strip()

    return s


def limpiar_nombre(s: str) -> str:
    if not s:
        return "SIN NOMBRE"
    s = str(s).strip()
    s = s.replace('"', "")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def reconstruir_fila(row):
    """
    Tu CSV está roto en algunas filas.
    Esta función intenta reconstruir:
    nombre_original, nombre_encontrado, direccion
    aunque se haya partido en más columnas.
    """

    if not row:
        return None

    # quitar columnas vacías al final
    while row and row[-1].strip() == "":
        row.pop()

    # caso normal: 3 columnas
    if len(row) == 3:
        return row[0], row[1], row[2]

    # si tiene más de 3, lo más común es:
    # nombre_original, nombre_encontrado, direccion_parte1, direccion_parte2, ...
    if len(row) > 3:
        nombre_original = row[0]
        nombre_encontrado = row[1]
        direccion = ",".join(row[2:])
        return nombre_original, nombre_encontrado, direccion

    # si tiene menos de 3, rellena
    if len(row) == 2:
        return row[0], row[1], ""
    if len(row) == 1:
        return row[0], "", ""

    return None


def main():
    lineas = []

    with open(INPUT_CSV, "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.reader(f)

        header = next(reader, None)  # saltar encabezado

        for row in reader:
            reconstruida = reconstruir_fila(row)
            if not reconstruida:
                continue

            nombre_original, nombre_encontrado, direccion = reconstruida

            nombre_original = limpiar_nombre(nombre_original)
            direccion = limpiar_direccion(direccion)

            lineas.append(f"\"{direccion}\", # {nombre_original}")

    with open(OUTPUT_TXT, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas))

    print(f"✅ Listo. Generado: {OUTPUT_TXT}")
    print(f"📌 Total líneas: {len(lineas)}")


if __name__ == "__main__":
    main()

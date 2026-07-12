# ==========================================================
# IMPORTACIÓN DE LIBRERÍAS
# ==========================================================

import cv2
import os
import numpy as np
from tqdm import tqdm


# ==========================================================
# CONFIGURACIÓN DEL REGISTRO DE DOCUMENTOS
# Permite evitar que un mismo documento sea procesado
# varias veces.
# ==========================================================

registro_path = "procesados.txt"

procesados = set()

if os.path.exists(registro_path):

    with open(registro_path, "r") as f:

        for linea in f:

            procesados.add(linea.strip())


# ==========================================================
# CONFIGURACIÓN DE CARPETAS
# ==========================================================

# Carpeta que contiene las imágenes preprocesadas

input_folder = (
    "C:/Users/rosai/OneDrive/Escritorio/"
    "legibilidad_documentos/dataset/preprocesado"
)

# Carpeta para documentos legibles

legible_folder = (
    "C:/Users/rosai/OneDrive/Escritorio/"
    "legibilidad_documentos/dataset/legible"
)

# Carpeta para documentos parcialmente legibles

parcial_folder = (
    "C:/Users/rosai/OneDrive/Escritorio/"
    "legibilidad_documentos/dataset/parcial"
)

# Carpeta para documentos ilegibles

ilegible_folder = (
    "C:/Users/rosai/OneDrive/Escritorio/"
    "legibilidad_documentos/dataset/ilegible"
)


# ==========================================================
# CREACIÓN DE CARPETAS DE SALIDA
# ==========================================================

os.makedirs(legible_folder, exist_ok=True)
os.makedirs(parcial_folder, exist_ok=True)
os.makedirs(ilegible_folder, exist_ok=True)


# ==========================================================
# FUNCIONES DE AUMENTO DE DATOS
# Cada función aplica un efecto para simular diferentes
# niveles de legibilidad.
# ==========================================================


# ----------------------------------------------------------
# EFECTO: SUCIEDAD
# Agrega manchas aleatorias sobre el documento.
# ----------------------------------------------------------

def dirty(image):

    img = image.copy()

    h, w = img.shape[:2]

    for i in range(40):

        x = np.random.randint(0, w)

        y = np.random.randint(0, h)

        r = np.random.randint(5, 20)

        color = (

            np.random.randint(0, 120),
            np.random.randint(0, 120),
            np.random.randint(0, 120)

        )

        cv2.circle(img, (x, y), r, color, -1)

    return img


# ----------------------------------------------------------
# EFECTO: SOMBRA
# Simula una sombra parcial sobre el documento.
# ----------------------------------------------------------

def shadow(image):

    h, w = image.shape[:2]

    mask = np.zeros((h, w), dtype=np.uint8)

    x = np.random.randint(0, w)

    cv2.rectangle(mask, (0, 0), (x, h), 255, -1)

    mask = cv2.GaussianBlur(mask, (101, 101), 0)

    shadow = image.copy()

    for i in range(3):

        shadow[:, :, i] = shadow[:, :, i] * (1 - mask / 255 * 0.6)

    return shadow.astype(np.uint8)


# ----------------------------------------------------------
# EFECTO: DISTORSIÓN
# Simula deformaciones del documento.
# ----------------------------------------------------------

def distortion(image):

    h, w = image.shape[:2]

    map_y, map_x = np.indices((h, w), dtype=np.float32)

    map_x = map_x + 20 * np.sin(map_y / 30)

    map_y = map_y + 20 * np.sin(map_x / 30)

    distorted = cv2.remap(
        image,
        map_x,
        map_y,
        cv2.INTER_LINEAR
    )

    return distorted


# ----------------------------------------------------------
# EFECTO: PIXELADO EXTREMO
# Reduce considerablemente la resolución.
# ----------------------------------------------------------

def extreme_pixelation(image):

    h, w = image.shape[:2]

    small = cv2.resize(
        image,
        (w // 20, h // 20)
    )

    pixelated = cv2.resize(
        small,
        (w, h),
        interpolation=cv2.INTER_NEAREST
    )

    return pixelated


# ==========================================================
# GENERACIÓN DEL DATASET
# ==========================================================

files = os.listdir(input_folder)

print("\n==========================================")
print(" Generando conjunto de datos...")
print("==========================================\n")


# ==========================================================
# RECORRER CADA DOCUMENTO DEL DATASET
# ==========================================================

for filename in tqdm(files, desc="Procesando documentos"):

    # ------------------------------------------------------
    # Verificar si el documento ya fue procesado
    # ------------------------------------------------------

    if filename in procesados:

        print("\nDocumento ya procesado. Se omite:", filename)

        continue

    # Procesar únicamente imágenes

    if filename.lower().endswith((".jpg", ".jpeg", ".png")):

        print(f"\nProcesando documento: {filename}")

        path = os.path.join(
            input_folder,
            filename
        )

        # --------------------------------------------------
        # Cargar la imagen
        # --------------------------------------------------

        image = cv2.imread(path)

        if image is None:

            print("Error cargando:", filename)

            continue


        # ==================================================
        # CLASE: LEGIBLE
        # Se conserva el documento sin modificaciones.
        # ==================================================

        print("Aplicando efecto: ORIGINAL (LEGIBLE)")

        cv2.imwrite(

            os.path.join(
                legible_folder,
                "legible_" + filename
            ),

            image

        )


        # ==================================================
        # CLASE: PARCIALMENTE LEGIBLE
        # ==================================================

        print("Aplicando efecto: SOMBRA")

        cv2.imwrite(

            os.path.join(
                parcial_folder,
                "shadow_" + filename
            ),

            shadow(image)

        )

        print("Aplicando efecto: SUCIO")

        cv2.imwrite(

            os.path.join(
                parcial_folder,
                "dirty_" + filename
            ),

            dirty(image)

        )


        # ==================================================
        # CLASE: ILEGIBLE
        # ==================================================

        print("Aplicando efecto: DISTORSIÓN")

        cv2.imwrite(

            os.path.join(
                ilegible_folder,
                "distortion_" + filename
            ),

            distortion(image)

        )

        print("Aplicando efecto: PIXELADO EXTREMO")

        cv2.imwrite(

            os.path.join(
                ilegible_folder,
                "pixelated_" + filename
            ),

            extreme_pixelation(image)

        )


        # ==================================================
        # REGISTRAR EL DOCUMENTO COMO PROCESADO
        # ==================================================

        with open(registro_path, "a") as f:

            f.write(filename + "\n")


# ==========================================================
# FIN DEL PROCESO
# ==========================================================

print("\n==========================================")
print(" Dataset generado correctamente")
print("==========================================")
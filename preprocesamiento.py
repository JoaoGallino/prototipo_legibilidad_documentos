# ==========================================================
# IMPORTACIÓN DE LIBRERÍAS
# ==========================================================

from PIL import Image

from tqdm import tqdm

import os


# ==========================================================
# CONFIGURACIÓN DE RUTAS
# ==========================================================

# Carpeta que contiene las imágenes originales.

input_folder = (
    "C:/Users/rosai/OneDrive/Escritorio/"
    "legibilidad_documentos/dataset/base"
)

# Carpeta donde se almacenarán las imágenes preprocesadas.

output_folder = (
    "C:/Users/rosai/OneDrive/Escritorio/"
    "legibilidad_documentos/dataset/preprocesado"
)

# Crear la carpeta de salida en caso de que no exista.

os.makedirs(output_folder, exist_ok=True)


# ==========================================================
# CONFIGURACIÓN DEL PREPROCESAMIENTO
# ==========================================================

# Tamaño máximo permitido para las imágenes.
# Se conserva automáticamente la relación de aspecto.

MAX_SIZE = (1400, 1400)


print("\n=============================================")
print(" Iniciando preprocesamiento de imágenes...")
print("=============================================\n")


# ==========================================================
# PREPROCESAMIENTO DE LAS IMÁGENES
# ==========================================================

# Se recorren todas las imágenes contenidas en la carpeta.

for filename in tqdm(
    os.listdir(input_folder),
    desc="Procesando imágenes"
):

    # Ruta de entrada y salida.

    input_path = os.path.join(
        input_folder,
        filename
    )

    output_path = os.path.join(
        output_folder,
        filename
    )

    try:

        # --------------------------------------------------
        # CARGAR LA IMAGEN
        # --------------------------------------------------

        image = Image.open(input_path)

        # --------------------------------------------------
        # REDIMENSIONAR LA IMAGEN
        # Mantiene la proporción automáticamente.
        # --------------------------------------------------

        image.thumbnail(MAX_SIZE)

        # --------------------------------------------------
        # GUARDAR LA IMAGEN PREPROCESADA
        # --------------------------------------------------

        image.save(
            output_path,
            quality=95
        )

    except Exception as e:

        print(
            f"Error al procesar {filename}: {e}"
        )


# ==========================================================
# FIN DEL PREPROCESAMIENTO
# ==========================================================

print("\n=============================================")
print(" Preprocesamiento completado correctamente")
print("=============================================")
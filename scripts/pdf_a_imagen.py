# ==========================================================
# IMPORTACIÓN DE LIBRERÍAS
# ==========================================================

from pdf2image import convert_from_path

import os


# ==========================================================
# CONFIGURACIÓN DE RUTAS
# ==========================================================

# Carpeta que contiene los documentos PDF

input_folder = (
    "C:/Users/rosai/OneDrive/Escritorio/"
    "legibilidad_documentos/dataset/pdf"
)

# Carpeta donde se almacenarán las imágenes generadas

output_folder = (
    "C:/Users/rosai/OneDrive/Escritorio/"
    "legibilidad_documentos/dataset/base"
)

# Ruta donde se encuentra instalada la biblioteca Poppler

poppler_path = "C:/poppler/Library/bin"


# ==========================================================
# CREAR LA CARPETA DE DESTINO
# ==========================================================

# Si la carpeta no existe, se crea automáticamente.

os.makedirs(output_folder, exist_ok=True)


# ==========================================================
# CONVERSIÓN DE DOCUMENTOS PDF A IMÁGENES
# ==========================================================

# Se recorren todos los archivos de la carpeta de entrada.

for file in os.listdir(input_folder):

    # Procesar únicamente archivos PDF.

    if file.endswith(".pdf"):

        # Ruta completa del documento PDF.

        pdf_path = os.path.join(
            input_folder,
            file
        )

        # Convertir todas las páginas del PDF en imágenes.

        pages = convert_from_path(
            pdf_path,
            poppler_path=poppler_path
        )

        # ==================================================
        # GUARDAR CADA PÁGINA COMO UNA IMAGEN JPG
        # ==================================================

        for i, page in enumerate(pages, start=1):

            image_name = (
                file.replace(".pdf", "")
                + f"_page{i}.jpg"
            )

            image_path = os.path.join(
                output_folder,
                image_name
            )

            # Guardar la imagen en formato JPG.

            page.save(
                image_path,
                "JPEG"
            )

            print(
                f"✓ Imagen guardada: {image_name}"
            )


# ==========================================================
# FIN DEL PROCESO
# ==========================================================

print("\nConversión finalizada correctamente.")
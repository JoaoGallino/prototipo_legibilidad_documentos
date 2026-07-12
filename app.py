from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session
)
from tensorflow.keras.models import load_model
from PIL import Image
from pdf2image import convert_from_path

import shutil  
import numpy as np
import os

app = Flask(__name__)

app.secret_key = "tesis_legibilidad_2026"

UPLOAD_FOLDER = "static/uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

USUARIO = "admin"
PASSWORD = "12345"

model = load_model(
    "modelo/keras_model.h5",
    compile=False
)

class_names = open(
    "modelo/labels.txt",
    "r",
    encoding="utf-8"
).readlines()

def preparar_imagen(imagen):

    image = imagen.convert("RGB")

    image = image.resize((224, 224))

    image_array = np.asarray(image)

    normalized_image_array = (
        image_array.astype(np.float32) / 127.5
    ) - 1

    data = np.ndarray(
        shape=(1, 224, 224, 3),
        dtype=np.float32
    )

    data[0] = normalized_image_array

    return data

def predecir(data):

    prediction = model.predict(data)

    index = np.argmax(prediction)

    class_name = class_names[index]

    confidence_score = prediction[0][index]

    resultado = class_name[2:].strip()

    if resultado.lower() == "legible":
        resultado = "Legible"

    elif resultado.lower() == "parcial":
        resultado = "Parcialmente legible"

    elif resultado.lower() == "ilegible":
        resultado = "Ilegible"

    return resultado, round(float(confidence_score) * 100, 2)


# ==========================
# LOGIN
# ==========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        usuario = request.form["usuario"]
        password = request.form["password"]

        if usuario == USUARIO and password == PASSWORD:

            session["usuario"] = usuario

            return redirect(url_for("index"))

        return render_template(
            "login.html",
            error="Usuario o contraseña incorrectos."
        )

    return render_template("login.html")


# ==========================
# CERRAR SESIÓN
# ==========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# ==========================
# LIMPIAR
# ==========================

@app.route("/limpiar")
def limpiar():

    carpeta = app.config["UPLOAD_FOLDER"]

    if os.path.exists(carpeta):

        for archivo in os.listdir(carpeta):

            ruta = os.path.join(carpeta, archivo)

            if os.path.isfile(ruta):

                os.remove(ruta)

    return redirect(url_for("index"))


# ==========================
# PRINCIPAL
# ==========================

@app.route("/", methods=["GET", "POST"])
def index():

    if "usuario" not in session:

        return redirect(url_for("login"))

    resultados = []

    total_legibles = 0
    total_parciales = 0
    total_ilegibles = 0

    if request.method == "POST":

        archivos = request.files.getlist("imagenes")

        for archivo in archivos:

            if archivo.filename == "":
                continue

            ruta = os.path.join(
                app.config["UPLOAD_FOLDER"],
                archivo.filename
            )

            archivo.save(ruta)

            extension = archivo.filename.lower()

            # -------------------
            # PDF
            # -------------------

            if extension.endswith(".pdf"):

                # Convierte todas las páginas del PDF
                paginas = convert_from_path(ruta)

                resultados_paginas = []

                confianzas_paginas = []

                detalle_paginas = []

                # Se utiliza la primera página como vista previa
                vista = os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    archivo.filename + "_preview.jpg"
                )

                paginas[0].save(vista)

                # Analizar cada página del documento
                for numero, pagina in enumerate(paginas, start=1):

                    data = preparar_imagen(pagina)

                    resultado_pagina, confianza_pagina = predecir(data)

                    resultados_paginas.append(resultado_pagina)

                    confianzas_paginas.append(confianza_pagina)

                    detalle_paginas.append({

                        "pagina": numero,

                        "resultado": resultado_pagina,

                        "confianza": confianza_pagina

                    })

                # Determinar la clasificación del documento completo
                if "Ilegible" in resultados_paginas:

                    resultado = "Ilegible"

                elif "Parcialmente legible" in resultados_paginas:

                    resultado = "Parcialmente legible"

                else:

                    resultado = "Legible"

                # Promedio de confianza de todas las páginas
                confianza = round(
                    sum(confianzas_paginas) / len(confianzas_paginas),
                    2
                )

            # -------------------
            # IMAGEN
            # -------------------

            else:

                imagen = Image.open(ruta)

                vista = ruta

                data = preparar_imagen(imagen)
            
                resultado, confianza = predecir(data)

                detalle_paginas = None

            # -------------------
            # PREDICCIÓN
            # -------------------
            
            if resultado == "Legible":
                color = "verde"

            elif resultado == "Parcialmente legible":
                color = "amarillo"

            else:
                color = "rojo"

            resultados.append({

                "nombre": archivo.filename,

                "imagen": vista,

                "resultado": resultado,

                "confianza": confianza,

                "color": color,

                "detalle": detalle_paginas if extension.endswith(".pdf") else None
            })
    
    total_legibles = sum(
    1 for doc in resultados
    if doc["resultado"] == "Legible"
    )

    total_parciales = sum(
    1 for doc in resultados
    if doc["resultado"] == "Parcialmente legible"
    )

    total_ilegibles = sum(
    1 for doc in resultados
    if doc["resultado"] == "Ilegible"
    )

    return render_template(

        "index.html",

        resultados=resultados,
        total_legibles=total_legibles,
        total_parciales=total_parciales,
        total_ilegibles=total_ilegibles
    )

if __name__ == "__main__":
    app.run(debug=True)
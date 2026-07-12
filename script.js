/* ==========================================================
   OBTENER LOS ELEMENTOS DE LA INTERFAZ
   Se obtienen los elementos que serán utilizados durante
   la interacción con la plataforma.
========================================================== */

const form = document.getElementById("upload-form");

const loading = document.getElementById("loading-container");


/* ==========================================================
   MOSTRAR EL INDICADOR DE CARGA
   Cuando el usuario envía uno o varios documentos para su
   análisis, se muestra una animación indicando que el
   proceso de clasificación está en ejecución.
========================================================== */

if (form && loading) {

    form.addEventListener("submit", () => {

        loading.style.display = "block";

    });

}


/* ==========================================================
   MOSTRAR U OCULTAR EL DETALLE DE LAS PÁGINAS
   Esta función permite visualizar la clasificación
   individual de cada página perteneciente a un documento
   PDF analizado.
========================================================== */

function mostrarDetalle(id) {

    const fila = document.getElementById("detalle" + id);

    if (!fila) {

        return;

    }

    if (fila.style.display === "none") {

        fila.style.display = "table-row";

    } else {

        fila.style.display = "none";

    }

}
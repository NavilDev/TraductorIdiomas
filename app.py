"""
app.py
---------
Este archivo define el servidor web Flask que actúa como backend de tu traductor.
Recibe peticiones POST desde el frontend, con un texto y los idiomas, y devuelve
la traducción en formato JSON.

Ejemplo de llamada:
POST /translate
{
  "source": "auto",
  "target": "en",
  "text": "Hola mundo"
}
"""

from flask import Flask, request, jsonify, render_template
from translator import Translator  # Importamos nuestra clase de traducción

# ------------------------------------------------------------
# Inicialización básica del servidor Flask
# ------------------------------------------------------------
app = Flask(__name__)

# Creamos una instancia del traductor (usa la API pública MyMemory)
translator = Translator()


# ------------------------------------------------------------
# ENDPOINT PRINCIPAL DE TRADUCCIÓN
# ------------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/translate", methods=["POST"])
def translate_route():
    """
    Recibe datos JSON y devuelve una traducción.
    Estructura esperada del JSON de entrada:
    {
      "source": "es" | "en" | "fr" | "de" | "pt" | "auto",
      "target": "es" | "en" | "fr" | "de" | "pt",
      "text": "Texto a traducir"
    }

    Devuelve JSON:
    {
      "translatedText": "...",
      "detectedSource": "es"   # opcional si se detectó automáticamente
    }
    """

    # Intentamos leer el JSON enviado por el frontend
    data = request.get_json(force=True, silent=True)
    if not data:
        # Si no hay JSON o viene vacío, respondemos con error 400 (Bad Request)
        return jsonify({"error": "JSON inválido o vacío"}), 400

    # Extraemos los campos
    source = data.get("source")
    target = data.get("target")
    text = data.get("text")

    # Validaciones básicas de los campos obligatorios
    if not target:
        return jsonify({"error": "Falta el campo 'target' (idioma destino)"}), 400
    if not text or not str(text).strip():
        return jsonify({"error": "Falta el campo 'text' o está vacío"}), 400

    # Si el usuario no especifica idioma origen, asumimos 'auto'
    if source is None:
        source = "auto"

    # Validamos los idiomas permitidos (los mismos que en el frontend)
    allowed = {"es", "en", "fr", "de", "pt", "auto"}
    if source not in allowed or target not in allowed - {"auto"}:
        return jsonify({"error": "Código de idioma no soportado"}), 400

    # Intentamos traducir
    try:
        result = translator.translate(source, target, text)
        return jsonify(result)  # Devolvemos el resultado en formato JSON
    except ValueError as ve:
        # Si hay error de validación (por ejemplo, texto vacío)
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        # Cualquier otro error inesperado
        return jsonify({"error": "Error interno en la traducción", "details": str(e)}), 500


# ------------------------------------------------------------
# PUNTO DE ENTRADA PRINCIPAL
# ------------------------------------------------------------
if __name__ == "__main__":
    # Flask se ejecuta en modo desarrollo y escucha en el puerto 5001
    # Cambia el puerto si ya está ocupado por otro proceso.
    app.run(host="0.0.0.0", port=5001, debug=True)
"""
translator.py
---------------
Este archivo define la clase `Translator`, responsable de:
- Detectar el idioma del texto de entrada.
- Enviar la petición de traducción a la API gratuita MyMemory.
- Manejar errores y devolver la respuesta al servidor Flask.
"""

import requests
from langdetect import detect, DetectorFactory

# Hacemos que langdetect sea determinista (para que no varíe entre ejecuciones)
DetectorFactory.seed = 0

# Idiomas soportados por la app (deben coincidir con los del frontend)
ALLOWED_LANGS = {"es", "en", "fr", "de", "pt"}


class Translator:
    """
    Clase principal encargada de traducir textos utilizando la API pública MyMemory.
    MyMemory no requiere autenticación ni instalación de librerías externas.
    """

    def __init__(self):
        # Endpoint base de la API
        self.api_url = "https://api.mymemory.translated.net/get"

    # ------------------------------------------------------------
    # DETECCIÓN DE IDIOMA
    # ------------------------------------------------------------
    def detect_language(self, text):
        """
        Usa la librería 'langdetect' para identificar el idioma del texto.
        Devuelve un código ISO de dos letras ('es', 'en', etc.).
        Si no puede detectarlo o el idioma no está permitido, devuelve None.
        """
        try:
            lang = detect(text)
            return lang if lang in ALLOWED_LANGS else None
        except Exception:
            # En caso de texto muy corto o error interno
            return None

    # ------------------------------------------------------------
    # FUNCIÓN PRINCIPAL DE TRADUCCIÓN
    # ------------------------------------------------------------
    def translate(self, source, target, text):
        """
        Traduce el texto usando la API MyMemory.

        Parámetros:
            source: idioma origen ('es', 'en', 'auto', etc.)
            target: idioma destino ('en', 'fr', etc.)
            text:   texto original

        Devuelve un diccionario con la estructura:
            {
                "translatedText": "...",
                "detectedSource": "es"  # opcional
            }
        """
        # Eliminamos espacios extra y validamos entrada
        text = (text or "").strip()
        if not text:
            raise ValueError("Texto vacío")

        # Verificamos que el idioma destino sea soportado
        if target not in ALLOWED_LANGS:
            raise ValueError(f"Idioma destino '{target}' no soportado")

        # Si el idioma origen es "auto", intentamos detectarlo
        detected = None
        if source == "auto":
            detected = self.detect_language(text)
            source_lang = detected if detected else "en"  # Por defecto 'en' si no detecta nada
        else:
            source_lang = source

        # ------------------------------------------------------------
        # Llamada a la API MyMemory
        # ------------------------------------------------------------
        # Ejemplo de URL: https://api.mymemory.translated.net/get?q=Hola&langpair=es|en
        params = {
            "q": text,
            "langpair": f"{source_lang}|{target}"
        }

        try:
            # Hacemos la petición HTTP GET
            resp = requests.get(self.api_url, params=params, timeout=10)
            resp.raise_for_status()  # Lanza excepción si la respuesta no es 200 OK

            data = resp.json()
            # Extraemos el texto traducido
            translated = data.get("responseData", {}).get("translatedText", "")

            if not translated:
                raise ValueError("No se obtuvo traducción válida de MyMemory")

            # Limpiamos comillas u otros caracteres extraños
            translated = translated.strip().strip('"')

            # Preparamos el resultado final
            meta = {"detectedSource": detected} if detected else {}
            return {"translatedText": translated, **meta}

        except Exception as e:
            # Si ocurre un error (sin conexión, timeout, etc.), devolvemos un mensaje indicativo
            simulated = f"[TRADUCCIÓN FALLIDA {source_lang}→{target}] {text}"
            meta = {"detectedSource": detected} if detected else {}
            return {"translatedText": simulated, **meta}
/**
 * main.js
 * ---------
 * Este archivo maneja toda la lógica del frontend:
 * - Captura el texto del usuario.
 * - Envía una petición POST al backend Flask (/translate).
 * - Muestra la traducción devuelta por el servidor.
 *
 * No requiere API keys ni configuraciones externas.
 * Solo necesita que Flask esté ejecutándose en http://127.0.0.1:5001
 */

// URL base del backend Flask
const API_URL = "http://127.0.0.1:5001/translate";

// Esperamos a que el DOM esté completamente cargado
document.addEventListener("DOMContentLoaded", () => {
  // Referencias a los elementos del DOM
  const sourceSelect = document.getElementById("sourceLang"); // Idioma origen
  const targetSelect = document.getElementById("targetLang"); // Idioma destino
  const textInput = document.getElementById("inputText");     // Texto original
  const resultBox = document.getElementById("result");        // Caja de resultado
  const translateBtn = document.getElementById("translateBtn"); // Botón "Traducir"

  /**
   * 🧩 Función principal: traduce el texto
   */
  async function translateText() {
    const text = textInput.value.trim();
    const source = sourceSelect.value;
    const target = targetSelect.value;

    // Validaciones rápidas en el frontend
    if (!text) {
      resultBox.innerText = "⚠️ Escribe algo para traducir.";
      return;
    }
    if (source === target) {
      resultBox.innerText = "⚠️ El idioma de origen y destino no pueden ser iguales.";
      return;
    }

    // Mostramos mensaje mientras esperamos la respuesta
    resultBox.innerText = "⏳ Traduciendo...";

    try {
      // Hacemos la petición POST al backend
      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          source,
          target,
          text
        })
      });

      // Parseamos la respuesta como JSON
      const data = await response.json();

      // Si el backend devuelve un error (por ejemplo, texto vacío)
      if (!response.ok || data.error) {
        throw new Error(data.error || "Error desconocido en el servidor");
      }

      // Mostramos la traducción real
      resultBox.innerHTML = `
        <strong>🗣️ Traducción (${data.detectedSource || source} → ${target}):</strong><br>
        ${data.translatedText}
      `;
    } catch (error) {
      // Si algo falla (red, backend, etc.)
      console.error("Error en la traducción:", error);
      resultBox.innerText = "❌ No se pudo traducir el texto. Revisa la conexión o el backend.";
    }
  }

  // Escuchamos el clic del botón "Traducir"
  translateBtn.addEventListener("click", translateText);

  // También permitimos traducir con Enter dentro del textarea
  textInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      translateText();
    }
  });
});
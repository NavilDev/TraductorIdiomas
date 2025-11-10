/**
 * main.js
 * ------------------
 * Controla toda la lógica del traductor:
 * - Envía peticiones al backend Flask (/translate)
 * - Muestra la traducción sin recargar la página
 * - Activa/desactiva el modo oscuro
 */

// URL del backend Flask
const API_URL = "http://127.0.0.1:5001/translate";

document.addEventListener("DOMContentLoaded", () => {
  // 🔤 Elementos del DOM
  const form = document.getElementById("translateForm");
  const sourceSelect = document.getElementById("sourceLang");
  const targetSelect = document.getElementById("targetLang");
  const textInput = document.getElementById("sourceText");
  const resultBox = document.getElementById("resultText");
  const swapBtn = document.getElementById("swapBtn");

  // 🌙 Elementos del modo oscuro
  const themeCheckbox = document.getElementById("themeCheckbox");
  const themeLabel = document.getElementById("themeLabel");

  // ---------------------------------------------------------
  // 🧩 FUNCIÓN PRINCIPAL DE TRADUCCIÓN
  // ---------------------------------------------------------
  form.addEventListener("submit", async (e) => {
    e.preventDefault(); // evita que el formulario recargue la página

    const text = textInput.value.trim();
    const source = sourceSelect.value;
    const target = targetSelect.value;

    // Validaciones rápidas
    if (!text) {
      resultBox.value = "⚠️ Escribe algo para traducir.";
      return;
    }
    if (source === target) {
      resultBox.value = "⚠️ El idioma de origen y destino no pueden ser iguales.";
      return;
    }

    resultBox.value = "⏳ Traduciendo...";

    try {
      // Petición al backend Flask
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ source, target, text }),
      });

      const data = await response.json();

      // Manejo de errores del servidor
      if (!response.ok || data.error) {
        throw new Error(data.error || "Error en el servidor.");
      }

      // Mostrar traducción limpia (sin etiquetas HTML)
      resultBox.value = data.translatedText;
    } catch (error) {
      console.error("Error en la traducción:", error);
      resultBox.value = "❌ No se pudo traducir el texto. Revisa la conexión o el backend.";
    }
  });

  // ---------------------------------------------------------
  // 🔄 INTERCAMBIAR IDIOMAS
  // ---------------------------------------------------------
  swapBtn.addEventListener("click", () => {
    const oldSource = sourceSelect.value;
    sourceSelect.value = targetSelect.value;
    targetSelect.value = oldSource;
  });

  // ---------------------------------------------------------
  // 🌙 MODO OSCURO
  // ---------------------------------------------------------
  // Cargar preferencia guardada
  const savedTheme = localStorage.getItem("theme");
  if (savedTheme === "dark") {
    document.documentElement.classList.add("dark");
    themeCheckbox.checked = true;
    themeLabel.textContent = "Modo oscuro";
  }

  // Escuchar cambios en el switch
  themeCheckbox.addEventListener("change", () => {
    if (themeCheckbox.checked) {
      document.documentElement.classList.add("dark");
      themeLabel.textContent = "Modo oscuro";
      localStorage.setItem("theme", "dark");
    } else {
      document.documentElement.classList.remove("dark");
      themeLabel.textContent = "Modo claro";
      localStorage.setItem("theme", "light");
    }
  });
});
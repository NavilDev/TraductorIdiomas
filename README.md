# 🌍 Traductor de Idiomas — Flask + MyMemory API

Aplicación web sencilla y gratuita que traduce textos entre varios idiomas  
utilizando la API pública **MyMemory** (sin necesidad de instalar dependencias externas de IA).

El proyecto está dividido en dos partes:
- 🧠 **Backend (Flask / Python)** → Procesa las solicitudes y llama a la API de traducción.  
- 🎨 **Frontend (HTML + CSS + JS)** → Interfaz web con formulario, selectores de idioma y resultado.

---

## 🚀 Funcionalidades

- Traducción entre los idiomas: **Español, Inglés, Francés, Alemán y Portugués**.  
- Detección automática del idioma de origen (`auto`).  
- Totalmente **gratuito y online** usando la API pública de MyMemory.  
- Frontend responsivo con modo claro/oscuro.  
- Backend ligero con Flask.

---

## 🧱 Estructura del Proyecto
TraductorIdiomas/
│
├── app.py                 # Servidor Flask principal
├── translator.py          # Lógica de traducción usando MyMemory
├── config.py              # Configuración global (puerto, URLs, etc.)
├── env.examples             # Configuración global (puerto, URLs, etc.)
│
├── requirements.txt       # Dependencias del entorno virtual
├── README.md              # Este archivo
│
├── venv/                  # Entorno virtual (creado localmente)
│
├── templates/
│   └── index.html         # Interfaz principal del traductor
│
└── static/
├── styles.css         # Estilos visuales del frontend
└── main.js            # Lógica JS para interactuar con el backend

## ⚙️ Instalación y Ejecución

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/traductor-idiomas.git
cd traductor-idiomas
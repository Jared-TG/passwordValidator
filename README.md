# 🔐 Generador y Validador de Contraseñas Seguras

Aplicación web construida con **Flask** que permite validar, generar y gestionar contraseñas seguras. Incluye una interfaz web moderna con tema oscuro, una API REST y pruebas automatizadas con **Behave** (BDD).

---

## 📋 Tabla de Contenidos

- [Descripción General](#-descripción-general)
- [Arquitectura del Proyecto](#-arquitectura-del-proyecto)
- [Tecnologías Utilizadas](#-tecnologías-utilizadas)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación y Ejecución](#-instalación-y-ejecución)
- [API REST – Endpoints](#-api-rest--endpoints)
- [Lógica de Negocio](#-lógica-de-negocio)
- [Pruebas Automatizadas (BDD)](#-pruebas-automatizadas-bdd)
- [Docker](#-docker)
- [Interfaz de Usuario](#-interfaz-de-usuario)

---

## 🧩 Descripción General

El proyecto ofrece tres funcionalidades principales:

| Funcionalidad | Descripción |
|---|---|
| **Validación manual** | El usuario ingresa una contraseña y el sistema le indica en tiempo real si cumple con las políticas de seguridad. |
| **Generación basada en palabras** | A partir de palabras clave proporcionadas por el usuario, se genera una contraseña segura que intenta mantener cierta legibilidad. |
| **Generación aleatoria** | Se genera una contraseña completamente aleatoria de 12 caracteres que cumple todas las reglas de seguridad. |

---

## 🏗 Arquitectura del Proyecto

```
Verificador/
├── app.py                         # Punto de entrada – servidor Flask y rutas API
├── src/
│   └── password_manager.py        # Lógica de negocio (validación y generación)
├── templates/
│   └── index.html                 # Interfaz web (HTML + CSS + JS embebido)
├── features/
│   ├── password.feature           # Escenarios BDD en Gherkin
│   └── steps/
│       └── password_steps.py      # Implementación de los pasos de prueba
├── Dockerfile                     # Imagen Docker para producción
├── docker-compose.yml             # Orquestación con Docker Compose
├── requirements.txt               # Dependencias de Python
└── .gitignore                     # Archivos ignorados por Git
```

### Flujo de la aplicación

```
┌──────────────┐     HTTP      ┌──────────────┐     import     ┌──────────────────────┐
│   Frontend   │ ────────────► │   app.py     │ ─────────────► │ password_manager.py  │
│  (index.html)│ ◄──────────── │   (Flask)    │ ◄───────────── │ (lógica de negocio)  │
└──────────────┘    JSON       └──────────────┘    dict/str     └──────────────────────┘
```

1. El **frontend** (`index.html`) envía peticiones HTTP a la API Flask.
2. **`app.py`** recibe las peticiones, las delega al módulo `password_manager`.
3. **`password_manager.py`** ejecuta la lógica de validación o generación y retorna el resultado.
4. `app.py` responde al frontend con JSON.

---

## 🛠 Tecnologías Utilizadas

| Tecnología | Propósito |
|---|---|
| **Python 3.10+** | Lenguaje principal del backend |
| **Flask** | Framework web para servir la API y el frontend |
| **Gunicorn** | Servidor WSGI para producción |
| **Behave** | Framework de pruebas BDD (Behavior-Driven Development) |
| **Docker** | Contenerización de la aplicación |
| **HTML/CSS/JS** | Interfaz de usuario (Single Page Application embebida) |

---

## ✅ Requisitos Previos

- **Python 3.10** o superior
- **pip** (gestor de paquetes de Python)
- **Docker** y **Docker Compose** (opcional, para ejecución contenerizada)

---

## 🚀 Instalación y Ejecución

### Ejecución local

```bash
# 1. Clonar el repositorio
git clone <URL_DEL_REPOSITORIO>
cd Verificador

# 2. Crear un entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate          # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la aplicación
python app.py
```

La aplicación estará disponible en: **http://localhost:5000**

### Ejecución con Docker

```bash
# Construir y levantar el contenedor
docker-compose up --build

# O usando Docker directamente
docker build -t verificador .
docker run -p 5000:5000 verificador
```

---

## 🌐 API REST – Endpoints

### `POST /api/validate`

Valida una contraseña contra las políticas de seguridad.

**Request:**
```json
{
  "password": "MiContraseña123!"
}
```

**Response (contraseña válida):**
```json
{
  "valid": true,
  "errors": []
}
```

**Response (contraseña inválida):**
```json
{
  "valid": false,
  "errors": [
    "Debe tener al menos 12 caracteres.",
    "Debe contener al menos un carácter especial."
  ]
}
```

---

### `POST /api/generate_words`

Genera una contraseña segura basada en palabras clave proporcionadas por el usuario.

**Request:**
```json
{
  "words": "mi perro salta"
}
```

**Response:**
```json
{
  "password": "miPerr0salt@!"
}
```

> **Nota:** La contraseña generada siempre cumple todas las políticas de seguridad. Si las palabras base no son suficientes (menos de 12 caracteres), se rellenan con caracteres adicionales.

---

### `GET /api/generate_random`

Genera una contraseña aleatoria de 12 caracteres que cumple todas las políticas.

**Response:**
```json
{
  "password": "aK9#mPx2$rLw"
}
```

---

## 🧠 Lógica de Negocio

El módulo `src/password_manager.py` contiene tres funciones principales:

### `validate_password(password: str) → dict`

Valida que la contraseña cumpla con **todas** las siguientes reglas:

| Regla | Descripción |
|---|---|
| Longitud mínima | Al menos **12 caracteres** |
| Mayúsculas | Al menos **1 letra mayúscula** (`A-Z`) |
| Minúsculas | Al menos **1 letra minúscula** (`a-z`) |
| Números | Al menos **1 dígito** (`0-9`) |
| Caracteres especiales | Al menos **1 carácter no alfanumérico** (ej: `!@#$%`) |

Retorna un diccionario con:
- `valid` (`bool`): `True` si cumple todas las reglas.
- `errors` (`list[str]`): Lista de mensajes de error por cada regla que no se cumple.

### `generate_from_words(words: str) → str`

1. Elimina los espacios de las palabras y las concatena.
2. Si la cadena resultante tiene menos de 12 caracteres, se rellena con caracteres aleatorios (letras, dígitos y símbolos).
3. Utiliza la función auxiliar `_ensure_requirements()` para garantizar que la contraseña resultante contenga al menos una mayúscula, una minúscula, un dígito y un carácter especial.
4. Itera hasta que la contraseña pase la validación.

### `generate_random() → str`

1. Genera una cadena aleatoria de 12 caracteres usando letras (mayúsculas y minúsculas), dígitos y símbolos de puntuación.
2. Valida la contraseña generada; si no cumple las reglas, genera otra hasta que sea válida.

### `_ensure_requirements(pwd_chars: list) → list`

Función auxiliar interna que reemplaza caracteres aleatorios de la lista con un carácter de cada categoría obligatoria (mayúscula, minúscula, dígito, especial), asegurando así que la contraseña cumpla las políticas.

---

## 🧪 Pruebas Automatizadas (BDD)

El proyecto utiliza **Behave** como framework de pruebas con enfoque BDD. Los escenarios están escritos en lenguaje Gherkin y se encuentran en `features/password.feature`.

### Escenarios de prueba

| Escenario | Descripción |
|---|---|
| Validar contraseña débil | Verifica que `"Hola123"` sea rechazada y muestre errores. |
| Validar contraseña segura | Verifica que `"SuperSegura123!"` sea aceptada sin errores. |
| Generar desde palabras | Genera una contraseña a partir de `"mi perro salta"` y valida que sea segura. |
| Generar aleatoria | Genera una contraseña aleatoria y valida que cumpla las políticas. |

### Ejecutar las pruebas

```bash
# Desde la raíz del proyecto
behave
```

**Salida esperada:**
```
4 features passed, 0 failed, 0 skipped
4 scenarios passed, 0 failed, 0 skipped
```

---

## 🐳 Docker

### Dockerfile

La imagen se basa en `python:3.10-slim` y utiliza **Gunicorn** como servidor WSGI para producción.

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD gunicorn app:app --bind 0.0.0.0:${PORT:-5000}
```

### docker-compose.yml

Configura un servicio `web` con:
- **Mapeo de puertos:** `5000:5000`
- **Volúmenes:** Monta el directorio actual en `/app` (para desarrollo).
- **Variables de entorno:** `FLASK_APP=app.py`, `FLASK_ENV=development`.

```bash
# Levantar
docker-compose up --build

# Detener
docker-compose down
```

---

## 🖥 Interfaz de Usuario

La interfaz web es una **Single Page Application** integrada directamente en `templates/index.html` con tema oscuro. Ofrece tres secciones:

### Sección 1 – Validación Manual
- El usuario escribe una contraseña en un campo de texto.
- La validación se ejecuta **en tiempo real** con un debounce de 300ms.
- Se muestran los errores de validación con iconos `✗` en rojo.
- Al cumplir todas las reglas, se muestra un mensaje de éxito `✓` en verde y se habilita el botón **"Guardar Contraseña"**.

### Sección 2 – Generación desde Palabras
- El usuario ingresa palabras clave (ej: `"mi perro salta"`).
- Al presionar el botón, se envía la petición a `/api/generate_words`.
- La contraseña generada se muestra en una caja con opción de **copiar al portapapeles**.

### Sección 3 – Generación Aleatoria
- Un solo botón que genera una contraseña aleatoria segura.
- La contraseña se muestra en una caja con opción de **copiar al portapapeles**.

---

## 📄 Licencia

Este proyecto es de uso educativo.

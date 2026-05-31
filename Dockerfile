FROM python:3.10-slim

WORKDIR /app

# Copiar requirements primero para aprovechar el caché de Docker
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Exponer el puerto de Flask
EXPOSE 5000

# El comando por defecto inicia la app con gunicorn
CMD gunicorn app:app --bind 0.0.0.0:${PORT:-5000}

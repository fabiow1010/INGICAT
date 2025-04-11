# Usa una imagen oficial de Python
FROM python:3.12-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia solo los archivos necesarios (excluyendo venv y SQLite)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del proyecto (pero venv y db.sqlite3 están ignorados en .dockerignore)
COPY . .

# Expone el puerto donde correrá Django
EXPOSE 8000

# Comando por defecto
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Usa una imagen base de Python
FROM python:3.10-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de tu aplicación al contenedor
COPY server/ .
COPY requirements.txt .
COPY source .
# Instala las dependencias de tu aplicación
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto en el que se ejecuta tu aplicación
EXPOSE 8000

# Ejecuta tu aplicación FastAPI cuando el contenedor se inicie
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

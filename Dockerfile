# Basis-Image mit Python 3.10
FROM python:3.10-slim

# Arbeitsverzeichnis im Container
WORKDIR /app

# Requirements kopieren und installieren
COPY requirements-docker.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements-docker.txt

# Projektdateien in den Container kopieren
COPY . .

# Standardbefehl: lokale Pipeline starten
CMD ["python", "dataflow_pipeline.py"]

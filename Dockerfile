# Basis: schlankes Python-Image
FROM python:3.11-slim

# Arbeitsverzeichnis im Container
WORKDIR /app

# Requirements kopieren & installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Skript ins Image kopieren
COPY dataflow_pipeline_local.py .

# Standard-Befehl beim Start des Containers
ENTRYPOINT ["python", "dataflow_pipeline_local.py"]

# Batch-basierte Auswertung von Blitzdaten

Dieses Projekt implementiert eine skalierbare, wartbare und zuverlässige Datenarchitektur zur Batch-basierten Verarbeitung von Blitzaktivitätsdaten.  
Die Architektur basiert auf Python-Skripten, Google Cloud Storage (GCS), einer Apache Beam Pipeline (DirectRunner) und BigQuery.  
Zur Sicherstellung von Reproduzierbarkeit wird die Pipeline zusätzlich in einem **Docker-Container** ausgeführt.  

Das Projekt wurde im Rahmen des IU-Kurses **Data Engineering (DLMDWWDE02)** umgesetzt.

---

## Architekturübersicht

**Datenfluss:**
1. CSV-Datei (`lightning_strikes_dataset.csv`) mit Blitzaktivitätsdaten.  
2. **Uploader-Skript (`uploader.py`)** validiert die Datei und lädt sie nach Google Cloud Storage (`gs://blitzdaten_us1/input/`).  
3. **Dataflow-Pipeline (`dataflow_pipeline.py`)** liest die CSV aus GCS, parst und bereinigt die Daten.  
4. Ergebnisse werden in **BigQuery** gespeichert (`blitzdaten_us1.lightning_strikes_us1_v2`).  
5. Die gesamte Pipeline ist auch als **Docker-Container** ausführbar, um eine konsistente Umgebung zu gewährleisten.  

**Komponenten:**
- Python 3.10  
- Apache Beam (DirectRunner = lokal)  
- Google Cloud Storage (Input-Datei, Temp-/Staging-Bucket)  
- BigQuery (Datenbank für Analyse und ML)  
- IAM & KMS für Sicherheit  
- Docker für Reproduzierbarkeit  

---

## ⚙️ Setup & Installation

### 1. Repository klonen

`git clone <REPO_URL>
cd Batch-basierte-Auswertung-von-Blitzdaten`

### 2. Virtuelle Umgebung erstellen (Python 3.10)

`python3.10 -m venv venv`  
`source venv/bin/activate`

### 3. Abhängigkeiten installieren

Für die lokale Entwicklung

`pip install -r requirements.txt`

Für den Docker-Container

`pip install -r requirements-docker.txt`

### 4. Mit Docker ausführen (Alternative zur lokalen Umgebung)

Image bauen

`docker build -t blitzdaten-pipeline .`

Pipeline starten (mit GCP Credentials):

`docker run --rm \
  -v $PWD/key.json:/app/key.json \
  -e GOOGLE_APPLICATION_CREDENTIALS="/app/key.json" \
  blitzdaten-pipeline`

## Nutzung der Skripte

### 1. Daten hochladen

Validieren & Upload der CSV nach GCS:

`python uploader.py`

### 2. Pipeline lokal ausführen (DirectRunner)

`python dataflow_pipeline.py`

Die Pipeline liest aus GCS, verarbeitet lokal (DirectRunner) und schreibt die Ergebnisse nach BigQuery.

## Ergebnisse prüfen

Nach dem erfolgreichen Pipeline-Lauf können die Ergebnisse in BigQuery abgefragt werden, z. B.:

```-- Anzahl der geladenen Zeilen
SELECT COUNT(*) 
FROM `agile-bonbon-470410-j2.blitzdaten_us1.lightning_strikes_us1_v2`;

-- Summe der Blitze pro Tag
SELECT date, SUM(number_of_strikes) AS strikes
FROM `agile-bonbon-470410-j2.blitzdaten_us1.lightning_strikes_us1_v2`
GROUP BY date
ORDER BY date ASC;
```

## Sicherheit

Zugriff auf GCS und BigQuery erfolgt ausschließlich über einen Service Account mit eingeschränkten Rollen:

`roles/storage.admin` (für GCS)

`roles/bigquery.dataEditor` (für BigQuery)

`roles/bigquery.jobUser` (zum Starten von Jobs)

Bucket und Dataset sind nicht öffentlich.

Daten werden automatisch durch Google Cloud verschlüsselt (KMS).

## Reproduzierbarkeit & Wartbarkeit

Versionskontrolle: gesamter Code im GitHub-Repository.

requirements.txt: ermöglicht reproduzierbare Python-Umgebung.

Dockerfile: Containerisiert die Pipeline → garantiert gleiche Umgebung auf jedem Rechner

Logging: Parsing-Fehler werden im Pipeline-Skript protokolliert.

Optionale Erweiterung: ein Dockerfile kann hinzugefügt werden, um die Pipeline in Containern laufen zu lassen.

## ML-Platform

Eine mögliche ML Platform (z. B. Vorhersagemodell für Blitzaktivitäten auf Basis der Daten) ist in dieser Architektur nicht Teil der Umsetzung.
BigQuery ist jedoch so vorbereitet, dass die Daten später für ML-Workflows (z. B. Vertex AI oder BigQuery ML) genutzt werden können.

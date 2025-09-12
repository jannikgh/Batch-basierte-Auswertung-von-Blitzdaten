# Batch-basierte Auswertung von Blitzdaten

Dieses Projekt implementiert eine **Batch-Datenpipeline** zur Verarbeitung von Blitzaktivitätsdaten auf Basis der **Google Cloud Platform (GCP)**.  
Die Architektur besteht aus folgenden Schritten:

1. **Upload**: Ein Python-Skript lädt CSV-Dateien mit Blitzdaten in einen Google Cloud Storage (GCS) Bucket.  
2. **Processing**: Ein Dataflow-Template (`CSV to BigQuery`) liest die CSV-Dateien, validiert und verarbeitet sie.  
3. **Storage**: Die bereinigten Daten werden in **BigQuery** gespeichert und stehen dort für Analysen oder Machine Learning (Out of Scope) bereit.  

---

## 📂 Repository-Inhalt
- `dataflow_pipeline.py` → Python-Skript für den Upload in GCS  
- `lightning_strikes_schema_bq.json` → BigQuery-Schema für die Tabelle  
- `requirements.txt` → Python-Abhängigkeiten (z. B. `google-cloud-storage`, `apache-beam[gcp]`)  
- `Dockerfile` → Containerisierung des Skripts  
- `LICENSE` → Apache-2.0 Lizenz  

---

## 🚀 Nutzung

1. Docker Image bauen
```bash
docker build -t lightning-uploader .
2. Hilfe anzeigen
bash
Code kopieren
docker run --rm lightning-uploader --help
3. CSV-Datei nach GCS hochladen
bash
Code kopieren
docker run --rm \
  -e GOOGLE_APPLICATION_CREDENTIALS=/creds/key.json \
  -v /Users/jannikgross-hardt/Desktop/Batch-basierte-Auswertung-von-Blitzdaten/key.json:/creds/key.json:ro \
  -v /Users/jannikgross-hardt/Desktop/Batch-basierte-Auswertung-von-Blitzdaten/lightning_strikes_dataset.csv:/data/file.csv:ro \
  lightning-uploader \
    --local-file /data/file.csv \
    --bucket blitzdaten_us1 \
    --dest-prefix input/ \
    --rename-with-timestamp

## 🔒 Sicherheit (IAM)
Für den Zugriff werden Service Accounts genutzt:

Zum Upload benötigt der Service Account mindestens die Rolle Storage Object Admin.

Für Lesezugriffe (Apache Beam) zusätzlich Storage Object Viewer.

## 📝 Lizenz
Dieses Projekt steht unter der Apache-2.0 Lizenz.

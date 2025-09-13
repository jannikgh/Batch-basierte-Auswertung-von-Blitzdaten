Batch-basierte Auswertung von Blitzdaten

Dieses Projekt implementiert eine skalierbare, wartbare und zuverlässige Datenarchitektur zur Batch-basierten Verarbeitung von Blitzaktivitätsdaten.
Die Architektur basiert auf Python-Skripten, Google Cloud Storage (GCS), einer Apache Beam Pipeline (DirectRunner) und BigQuery.

Das Projekt wurde im Rahmen des IU-Kurses Data Engineering (DLMDWWDE02) umgesetzt.

Architekturübersicht

Datenfluss:

CSV-Datei (lightning_strikes_dataset.csv) mit Blitzaktivitätsdaten.

Uploader-Skript (uploader.py) validiert die Datei und lädt sie nach Google Cloud Storage (gs://blitzdaten_us1/input/).

Dataflow-Pipeline (dataflow_pipeline.py) liest die CSV aus GCS, parst und bereinigt die Daten.

Ergebnisse werden in BigQuery gespeichert (blitzdaten_us1.lightning_strikes_us1_v2).

Komponenten:

Python 3.10

Apache Beam (DirectRunner = lokal)

Google Cloud Storage (Input-Datei, Temp-/Staging-Bucket)

BigQuery (Datenbank für Analyse und ML)

IAM & KMS für Sicherheit

Setup & Installation

Repository klonen:
git clone <REPO_URL>
cd Batch-basierte-Auswertung-von-Blitzdaten

Virtuelle Umgebung erstellen (Python 3.10):
python3.10 -m venv venv
source venv/bin/activate

Abhängigkeiten installieren:
pip install -r requirements.txt

Die Datei requirements.txt enthält alle Pakete und Versionen, die für das Projekt benötigt werden (z. B. apache-beam[gcp], google-cloud-storage, google-cloud-bigquery).
Damit kann die Umgebung jederzeit reproduziert werden.

Nutzung der Skripte

Daten hochladen:
python uploader.py

Pipeline lokal ausführen (DirectRunner):
python dataflow_pipeline.py

Die Pipeline liest aus GCS, verarbeitet lokal (DirectRunner) und schreibt die Ergebnisse nach BigQuery.

Ergebnisse prüfen

Nach dem erfolgreichen Pipeline-Lauf können die Ergebnisse in BigQuery abgefragt werden, z. B.:

Anzahl der geladenen Zeilen:
SELECT COUNT(*)
FROM agile-bonbon-470410-j2.blitzdaten_us1.lightning_strikes_us1_v2;

Summe der Blitze pro Tag:
SELECT date, SUM(number_of_strikes) AS strikes
FROM agile-bonbon-470410-j2.blitzdaten_us1.lightning_strikes_us1_v2
GROUP BY date
ORDER BY date ASC;

Sicherheit

Zugriff auf GCS und BigQuery erfolgt ausschließlich über einen Service Account mit eingeschränkten Rollen:

roles/storage.admin (für GCS)

roles/bigquery.dataEditor (für BigQuery)

Bucket und Dataset sind nicht öffentlich.

Daten werden automatisch durch Google Cloud verschlüsselt (KMS).

Reproduzierbarkeit & Wartbarkeit

Versionskontrolle: gesamter Code im GitHub-Repository.

requirements.txt: ermöglicht reproduzierbare Python-Umgebung.

Logging: Parsing-Fehler werden im Pipeline-Skript protokolliert.

Optionale Erweiterung: ein Dockerfile kann hinzugefügt werden, um die Pipeline in Containern laufen zu lassen.

Hinweise

Das Projekt wurde mit DirectRunner (lokal) umgesetzt, wie in der Prüfungsaufgabe gefordert.

Zusätzlich wurde die Pipeline erfolgreich mit DataflowRunner (Cloud) getestet, wobei Einschränkungen durch IAM-Policies berücksichtigt werden mussten.

Damit ist die Architektur sowohl prüfungsrelevant (lokal) als auch realistisch (Cloud) nutzbar.

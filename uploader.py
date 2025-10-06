import configparser
from google.cloud import storage
import os
import csv
from pathlib import Path

# Erwartete Header
EXPECTED_HEADER = ["date", "number_of_strikes", "center_point_geom"]

# Fester Eingabeordner
LOCAL_INPUT_DIR = None

# Ziel-Bucket und Pfad in GCS
BUCKET_NAME = None
GCS_PREFIX = "input/"

# Service Account Credentials
CREDENTIALS = "key.json"

def read_config():
    if not Path("./config.ini").exists():
        raise Exception("❌ Config nicht gefunden.")
    config = configparser.ConfigParser()
    config.read("config.ini")
    path_from_config = config.get("Uploader", "input_dir")
    global LOCAL_INPUT_DIR
    LOCAL_INPUT_DIR = Path(path_from_config)
    global BUCKET_NAME
    BUCKET_NAME = config.get("Uploader", "bucket_name")


def validate_csv(file_path: Path) -> bool:
    """Validiert eine CSV-Datei anhand Kopfzeile und Spalten."""
    try:
        with file_path.open(newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)
            number_of_columns = len(EXPECTED_HEADER)
            if header != EXPECTED_HEADER:
                raise Exception (f"❌ {file_path.name}: Header ungültig. Gefunden: {header}")
            for i, row in enumerate(reader, 2):
                if len(row) != number_of_columns:
                    raise Exception (f"❌ {file_path.name}: Zeile {i} hat nicht die vorgegebene Anzahl ({number_of_columns}) an Spalten.")
                int(row[1])  # number_of_strikes muss int sein
                if not row[0]:
                    raise Exception (f"❌ {file_path.name}: Zeile {i} enthält kein Datum.")
        return True
    except Exception as e:
        print(f"❌ {file_path.name}: Fehler bei Validierung: {e}")
        return False


def upload_to_gcs(file_path: Path):
    """Lädt eine Datei in den GCS-Bucket hoch."""
    client = storage.Client.from_service_account_json(CREDENTIALS)
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(f"{GCS_PREFIX}{file_path.name}")
    blob.upload_from_filename(str(file_path))
    print(f"✅ Hochgeladen: {file_path.name} → gs://{BUCKET_NAME}/{GCS_PREFIX}{file_path.name}")


def main():
    read_config()
    if not LOCAL_INPUT_DIR.exists():
        raise Exception(f"❌ Ordner {LOCAL_INPUT_DIR} nicht gefunden.")

    csv_files = [f for f in LOCAL_INPUT_DIR.glob("*.csv")]
    if not csv_files:
        raise Exception(f"❌ Keine CSV-Dateien in {LOCAL_INPUT_DIR} gefunden.")

    print(f"Gefundene Dateien: {[f.name for f in csv_files]}")

    for csv_file in csv_files:
        if validate_csv(csv_file):
            upload_to_gcs(csv_file)
        else:
            print(f"⚠️ Datei übersprungen: {csv_file.name}")


if __name__ == "__main__":
    main()

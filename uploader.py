from google.cloud import storage
import os
import csv

def validate_csv(file_path):
    """Prüft die CSV-Datei auf Struktur und Datentypen"""
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # erste Zeile = Spaltennamen
        
        # Erwartete Spalten
        expected_header = ["date", "number_of_strikes", "center_point_geom"]
        if header != expected_header:
            raise ValueError(f"❌ Ungültiges CSV-Format!\n"
                             f"Gefunden: {header}\n"
                             f"Erwartet: {expected_header}")
        
        # Erste paar Zeilen prüfen
        for i, row in enumerate(reader, start=2):  # start=2 weil header = Zeile 1
            if len(row) != 3:
                raise ValueError(f"❌ Zeile {i} hat nicht 3 Spalten: {row}")
            
            # Prüfen: number_of_strikes ist Zahl
            try:
                int(row[1])
            except ValueError:
                raise ValueError(f"❌ Zeile {i}: number_of_strikes ist keine Zahl -> {row[1]}")
            
            # Optional: date-Feld prüfen (nur auf Leerstring hier)
            if not row[0]:
                raise ValueError(f"❌ Zeile {i}: leeres Datumsfeld")
            
            # Prüfung der ersten 100 Zeilen für Performance
            if i > 100:
                break

    print("✅ CSV-Format und Beispieldaten geprüft: OK")

def upload_to_gcs(bucket_name, source_file, destination_blob):
    """Lädt eine Datei in einen GCS Bucket hoch"""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob)
    
    blob.upload_from_filename(source_file)
    print(f"✅ Datei {source_file} wurde als {destination_blob} in {bucket_name} hochgeladen.")

if __name__ == "__main__":
    # Lokale CSV-Datei
    source_file = "/Users/jannikgross-hardt/Desktop/Batch-basierte-Auswertung-von-Blitzdaten/lightning_strikes_dataset.csv"
    
    # Ziel in GCS
    bucket_name = "blitzdaten_us1"
    destination_blob = "input/blitzdaten.csv"
    
    # Service Account Key einlesen
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"
    
    # 1. Validierung
    validate_csv(source_file)
    
    # 2. Upload
    upload_to_gcs(bucket_name, source_file, destination_blob)

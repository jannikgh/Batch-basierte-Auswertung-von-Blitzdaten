import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, GoogleCloudOptions, StandardOptions
import csv
import logging
from datetime import datetime


class ParseCSVLine(beam.DoFn):
    def process(self, element):
        try:
            # CSV-Zeile in Felder splitten
            fields = list(csv.reader([element]))[0]

            # Felder ins richtige Format bringen
            parsed_record = {
                # Datum in BQ-kompatibles Date-Format (YYYY-MM-DD)
                'date': datetime.strptime(fields[0], "%Y-%m-%d").date().isoformat(),

                # Integer bleibt Integer
                'number_of_strikes': int(fields[1]),

                # Geography als Well Known Text (WKT)
                # Erwartet: fields[2] enthält "lon lat"
                'center_point_geom': f"POINT({fields[2]})"
            }
            return [parsed_record]

        except Exception as e:
            logging.error(f"Fehler beim Parsen: {e} | Zeile: {element}")
            return []


def run():
    # Pipeline Optionen
    options = PipelineOptions()
    google_cloud_options = options.view_as(GoogleCloudOptions)
    google_cloud_options.project = "agile-bonbon-470410-j2" 
    google_cloud_options.region = "europe-west3"                 
    google_cloud_options.staging_location = "gs://blitzdaten_us1/tmp/staging"
    google_cloud_options.temp_location = "gs://blitzdaten_us1/tmp"
    options.view_as(StandardOptions).runner = "DirectRunner"

    # Pipeline Definition
    with beam.Pipeline(options=options) as p:
        (
            p
            | "Read CSV" >> beam.io.ReadFromText("gs://blitzdaten_us1/input/blitzdaten.csv", skip_header_lines=1)
            | "Parse CSV" >> beam.ParDo(ParseCSVLine())
            | "Write to BigQuery" >> beam.io.WriteToBigQuery(
                table="blitzdaten_us1.lightning_strikes_us1_v2",
                schema="date:DATE, number_of_strikes:INTEGER, center_point_geom:GEOGRAPHY",
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED
            )
        )


if __name__ == "__main__":
    run()

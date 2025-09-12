import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, GoogleCloudOptions, StandardOptions
import csv
import logging

class ParseCSVLine(beam.DoFn):
    def process(self, element):
        try:
            fields = list(csv.reader([element]))[0]
            return [{
                'date': fields[0],
                'number_of_strikes': int(fields[1]),
                'center_point_geom': fields[2]
            }]
        except Exception as e:
            logging.error(f"Fehler beim Parsen: {e}")
            return []

def run():
    options = PipelineOptions()
    google_cloud_options = options.view_as(GoogleCloudOptions)
    google_cloud_options.project = 'agile-bonbon-470410-j2'
    google_cloud_options.region = 'europe-west3'
    google_cloud_options.job_name = 'csv-to-bq-blitzdaten'
    google_cloud_options.staging_location = 'gs://blitzdaten_us1/tmp/staging'
    google_cloud_options.temp_location = 'gs://blitzdaten_us1/tmp'
    options.view_as(StandardOptions).runner = 'DataflowRunner'

    with beam.Pipeline(options=options) as pipeline:
        (
            pipeline
            | 'CSV lesen' >> beam.io.ReadFromText('gs://blitzdaten_us1/input/lightning_strikes_dataset.csv', skip_header_lines=1)
            | 'Parsen' >> beam.ParDo(ParseCSVLine())
            | 'Nach BigQuery schreiben' >> beam.io.WriteToBigQuery(
                table='blitzdaten.lightning_strikes',
                dataset='blitzdaten',
                project='agile-bonbon-470410-j2',
                schema='date:DATE,number_of_strikes:INTEGER,center_point_geom:STRING',
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
                create_disposition=beam.io.BigQueryDisposition.CREATE_NEVER
            )
        )

if __name__ == '__main__':
    run()
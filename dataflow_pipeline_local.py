import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
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
    options.view_as(StandardOptions).runner = 'DirectRunner'  # Nur lokal

    with beam.Pipeline(options=options) as pipeline:
        parsed = (
            pipeline
            | 'CSV lesen' >> beam.io.ReadFromText('/data/file.csv', skip_header_lines=1)
            | 'Parsen' >> beam.ParDo(ParseCSVLine())
        )

        # Ausgabe der Rohdaten (zur Kontrolle)
        parsed | 'Rohdaten ausgeben' >> beam.Map(print)

        # Aggregation: Anzahl Blitze pro Datum
        (
            parsed
            | 'Key nach Datum' >> beam.Map(lambda x: (x['date'], x['number_of_strikes']))
            | 'Summe pro Datum' >> beam.CombinePerKey(sum)
            | 'Aggregat ausgeben' >> beam.Map(lambda x: print(f"Datum: {x[0]}, Blitze gesamt: {x[1]}"))
        )

if __name__ == '__main__':
    run()

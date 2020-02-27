import click
import boto3
import gzip
import json
import pyjq

from io import BytesIO

@click.command(help="Get a trip file from S3 and output a link to Google maps of the trip")
@click.argument('trip_bucket_name')
@click.argument('trip_file_name')
def maptrip(trip_bucket_name, trip_file_name):
    file_contents = get_data_file(trip_file_name)
    json_contents = json.loads(file_contents)
    trip_info = pyjq.all('.locations | first.timestamp |= todateiso8601 | last.timestamp |= todateiso8601 | "start: \(first.timestamp)", "end: \(last.timestamp)", "map: https://google.com/maps/dir/\(first.latitude),\(first.longitude)/\(last.latitude),\(last.longitude)"', json_contents)
    for obj in trip_info:
        click.echo(obj)

def get_data_file(trip_file_name):
    s3 = boto3.resource('s3')
    response_object = s3.Object(trip_bucket_name, trip_file_name).get()
    object_body = response_object['Body'].read()
    gzipfile = BytesIO(object_body)
    gzip_file_handle = gzip.GzipFile(fileobj=gzipfile)
    return gzip_file_handle.read()
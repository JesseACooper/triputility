import click
import os
import sys
import boto3
import gzip
import json
import pyjq

from io import BytesIO
from journey.utils import condition_builder, compose_query, get_trip_info, parse_trip_info

@click.command(name="map", help="Get a trip file from S3 and output a link to Google maps of the trip")
@click.option('--id', '-i', type=str, help="The id of the trip")
@click.option('--data-file-name', '-d', type=str, help="The data file name of the trip")
@click.option('--trip-bucket', type=str, help="The name of the s3 bucket to look in")
@click.pass_obj
def map_(client, id, data_file_name, trip_bucket):
    aws_key = os.environ.get('AWS_ACCESS_KEY_ID')
    if not aws_key:
        click.echo("Aborting: AWS credentials not set - did you run aws-login?")
        sys.exit()

    if not data_file_name and not id:
        click.echo("No identifying information for trip provided, aborting")
        sys.exit()

    trip_info = fetch_trip_info(client, id=id, data_file_name=data_file_name)
    id = trip_info['id']
    data_file_name = trip_info['data_file_name']

    if not trip_bucket:
        trip_bucket = trip_info['trip_bucket']

    print_mapping(trip_bucket, data_file_name)

def fetch_trip_info(client, id, data_file_name):
    condition = condition_builder(id=id, data_file_name=data_file_name)
    query = compose_query(condition)
    return parse_trip_info(get_trip_info(client, query))

def print_mapping(trip_bucket, data_file_name):
    file_contents = get_data_file(trip_bucket, data_file_name)
    if not file_contents:
        click.echo("Could not retrieve file contents from S3, likely due to expired AWS tokens. Aborting.")
        sys.exit()

    json_contents = json.loads(file_contents)
    map_url = pyjq.all('.locations | "https://google.com/maps/dir/\(first.latitude),\(first.longitude)/\(last.latitude),\(last.longitude)"', json_contents)[0]
    click.echo(map_url)

def get_data_file(trip_bucket, data_file_name):
    try:
        s3 = boto3.resource('s3')
        response_object = s3.Object(trip_bucket, data_file_name).get()
        object_body = response_object['Body'].read()
        gzipfile = BytesIO(object_body)
        gzip_file_handle = gzip.GzipFile(fileobj=gzipfile)
        return gzip_file_handle.read()
    except Exception as e:
        click.echo(e)

import click
import json

from journey.utils import condition_builder, compose_query, get_trip_info, parse_trip_info

@click.command(help="Retrieve information about a trip from Redash")
@click.option('--id', '-i', type=str, help="The id of the trip")
@click.option('--data-file-name', '-d', type=str, help="The data file name of the trip")
@click.option('--verbose', '-v', is_flag=True, default=False, help="Displays the full trip info in a JSON blob")
@click.pass_obj
def info(client, id, data_file_name, verbose):
    if not data_file_name and not id:
        click.echo("No identifying information for trip provided, aborting")
        sys.exit()

    condition = condition_builder(id=id, data_file_name=data_file_name)
    query = compose_query(condition)
    trip_info = parse_trip_info(get_trip_info(client, query))

    if not verbose:
        trip_info = important_info_only(trip_info)

    click.echo(json.dumps(trip_info, indent=4))

def important_info_only(trip_info):
    important_info = {
        'id': trip_info['id'],
        'data_file_name': trip_info['data_file_name'],
        'trip_bucket': trip_info['trip_bucket'],
        'telematics_user_id': trip_info['telematics_user_id'],
        'telematics_application_name': trip_info['telematics_application_name'],
        'distance': trip_info['distance'],
        'created_at': trip_info['created_at']
    }
    return important_info
import click
import sys

GET_TRIP_QUERY_NAME = "Journey query"

QUERY_RETURN_FIELDS = "trips.*, telematics_application_id, telematics_applications.name as telematics_application_name, trip_bucket"
QUERY_JOINS = "trips join telematics_users on trips.telematics_user_id = telematics_users.id join telematics_applications on telematics_users.telematics_application_id = telematics_applications.id"

def get_trip_info(client, trip_query):
    response = client.post(
        "queries",
        dict(query=trip_query, data_source_id=7090, name=GET_TRIP_QUERY_NAME)
    )

    query_id = response.get("id")
    data = perform_download(client, query_id)

    return data

def perform_download(client, query_id):
    job_id = client.post(f"queries/{query_id}/refresh").get("job").get("id")
    query_result_id = client.poll(f"jobs/{job_id}").get("job").get("query_result_id")
    return client.get(f"queries/{query_id}/results/{query_result_id}.json")

def condition_builder(id, data_file_name):
    if not id:
        return f"trips.data_file_name like \'%{data_file_name}%\'"
    else:
        return f"trips.id = \'{id}\'"

def compose_query(condition):
    return f"select {QUERY_RETURN_FIELDS} from {QUERY_JOINS} where {condition}"

def parse_trip_info(trip_info):
    rows = trip_info['query_result']['data']['rows']
    if len(rows) > 1:
        click.echo("More than one trip found, please select from the below list by entering its index:")
        for index, trip_info in enumerate(rows):
            click.echo(f"{index}: id: {trip_info['id']} | data_file_name: {trip_info['data_file_name']}")

        value = -1
        valid_index_input = False
        while not valid_index_input:
            value = click.prompt('Please enter a valid integer index', type=int)
            if value >= 0 and value <= len(rows) - 1:
                valid_index_input = True
            else:
                click.echo("Invalid index")

        click.echo(f"Selecting trip at index {value}")
        return rows[value]
    elif len(rows) < 1:
        click.echo("No results found, aborting")
        sys.exit()
    else:
        return rows[0]

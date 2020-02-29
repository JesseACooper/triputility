GET_TRIP_QUERY_NAME = "Triputility query"

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
    return f"select trips.*, telematics_application_id, telematics_applications.name as telematics_application_name, trip_bucket from trips join telematics_users on trips.telematics_user_id = telematics_users.id join telematics_applications on telematics_users.telematics_application_id = telematics_applications.id where {condition} limit 1"

def parse_trip_info(trip_info):
    return trip_info['query_result']['data']['rows'][0]

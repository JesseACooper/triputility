# Journey CLI

Journey is a CLI for getting information about a particular trip. Once configured, you can pass a trip id or data file name and get information about the trip (such as distance, device, trip bucket, etc.).

You can also infer new information about a trip, e.g. generate a Google Maps URL that approximates the route of the trip.

## Configuring

Trip querying is handled via Redash - as such, you will need to supply a Redash API key. There are two ways to do this:

### ~/.journey-cli.ini

Create a `.journey-cli.ini` file in your home directory and give it the following contents:

```
[DEFAULT]
redash_api_key = YOUR_API_KEY
```

### config.ini

You can also create a `config.ini` file in the app directory, if you clone and run from the repo. The contents should be identical to the above. If you have both set up, values in `config.ini` will overwrite what's in `.journey-cli.ini`.

## Usage

Journey currently has two commands: `info`, which displays information about a trip, and `map`, which generates a Google Maps URL mapping the approximate trip route.

You can supply either command a trip's id, or its data_file_name. If both are supplied, id is used. When specifying id, you must supply the whole id; when specifying data_file_name, only a partial match is required. If multiple matches are found, you will be prompted to select which you are interested in.

### info example

```bash
$ journey info --data-file-name 1234abcd
>> {
    "id": "some-trip-id",
    "data_file_name": "1234abcd-5678efgh.json.gz",
    "trip_bucket": "staging-trip-bucket",
    "telematics_user_id": "some-telematics-trip-id",
    "telematics_application_name": "scott-o-seguro",
    "distance": 0.555111,
    "created_at": "2020-02-28T18:00:00.000"
}
```

You can optionally supply a `--verbose` (or simply `-v`) flag to info and it will return the full JSON blob we get from the database (e.g. `updated_at`) instead of the truncated result set above.

```bash
$ journey info --verbose --data-file-name 1234abcd
>> {
  "a-large-json-blob": [. . .]
}
```

### map example

Before running `map`, you will need to run `aws-login` with the appropriate role in the same console.

```bash
$ journey map --data-file-name 1234abcd
>> https://www.google.com/maps/dir/FIRST_WAYPOINT.lat,-FIRST_WAYPOINT.long/LAST_WAYPOINT.lat,-LAST_WAYPOINT.long
```

It is worth noting that this will only approximately map out the trip, as it only looks at the first and last points on a trip. This will result in progressively lossier, less accurate data as trips are longer and take more complicated routes.

You may optionally provide a trip bucket name to the command - if not, however, it will be inferred from the trip data acquired from Redash.

```bash
$ journey map --data-file-name 1234abcd --trip-bucket staging-trip-bucket
>> https://www.google.com/maps/dir/FIRST_WAYPOINT.lat,-FIRST_WAYPOINT.long/LAST_WAYPOINT.lat,-LAST_WAYPOINT.long
```

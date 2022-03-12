import datetime
import json
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.client.flux_table import FluxStructureEncoder
from flask import Blueprint, jsonify, request, current_app
from werkzeug.exceptions import BadRequest, NotFound


client = InfluxDBClient(url="http://localhost:8086", token="uw", org="University of Washington")
client_write_api = client.write_api(write_options=SYNCHRONOUS)
client_query_api = client.query_api()

weight_scale_blueprint_instance = Blueprint(name='weight_scale', import_name=__name__, url_prefix='/weight')


def calc_mean(table):
    records = table['records']
    m = 0
    for r in records:
        m += r['values']['_value']
    return m / len(records)


@weight_scale_blueprint_instance.route('/')
def get_weight():
    # Get query string
    start_time = int(request.args.get('startTime'))
    name = request.args.get('name')
    if not start_time:
        return BadRequest('startTime should be provided')
    if not name:
        return BadRequest('Name should be provided')
    # Query the weight of the food at starting time
    tables = client_query_api.query(f'from(bucket: "final")\
        |> range(start:{start_time}, stop:{start_time + 10})\
        |> filter(fn: (r) => r._measurement == "pet_feeder")\
    ')
    tables = json.loads(json.dumps(tables, cls=FluxStructureEncoder, indent=2))
    current_app.logger.info(tables)
    if len(tables) == 0:
        return NotFound('The table is empty')

    m_origin = calc_mean(tables[0])

    # Query the weight of the food for now-1m ~ now-30s and now-30s to now
    # If they are the same, write to the database
    tables_previous = client_query_api.query(f'from(bucket: "final")\
            |> range(start:-2m, stop:now())\
            |> filter(fn: (r) => r._measurement == "pet_feeder")\
            |> window(every: 1m)')

    # Convert FluxTable to Json
    tables_previous = json.loads(json.dumps(tables_previous, cls=FluxStructureEncoder, indent=2))
    m1 = calc_mean(tables_previous[0])
    m2 = calc_mean(tables_previous[1])
    if abs(m1 - m2) <= 200:
        # Calculate the difference
        m_r = m_origin - ((m2 + m2) / 2)
        # write to the database
        d = {
            "measurement": "pet_feeder_tags",
            "fields": {
                "consumed_weight": m_r
            },
            "tags": {
                "name": name
            }
        }
        p = Point.from_dict(d)
        # Write to influxdb
        client_write_api.write(bucket="final", record=p)
        return jsonify({
            "isFinished": True,
        })
    return jsonify({
            "isFinished": False,
        })

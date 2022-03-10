import datetime
import json
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.client.flux_table import FluxStructureEncoder
from flask import Blueprint, jsonify, request, current_app
from hx711py.driver import hx


client = InfluxDBClient(url="http://localhost:8086", token="uw", org="University of Washington")
client_write_api = client.write_api(write_options=SYNCHRONOUS)
client_query_api = client.query_api()

weight_scale_blueprint_instance = Blueprint(name='weight_scale', import_name=__name__, url_prefix='/weight')


@weight_scale_blueprint_instance.route('/')
def get_weight():
    hx.GP_LOCK.acquire(blocking=True, timeout=2)
    weight = hx.val
    hx.GP_LOCK.release()
    # Get query string
    start_time = request.args.get('startTime')
    if not start_time:
        start_time = datetime.datetime.timestamp(datetime.datetime.now())

    tables = client_query_api.query('from(bucket: "final")\
        |> range(start: -1d)\
        |> filter(fn: (r) => r._measurement == "pet_feeder")\
    ')
    output = json.dumps(tables, cls=FluxStructureEncoder, indent=2)
    current_app.logger(output)
    return output

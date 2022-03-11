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


def calc_mean(table):
    records = table['records']
    m = 0
    for r in records:
        m += r['values']['_value']
    return m / len(records)


@weight_scale_blueprint_instance.route('/')
def get_weight():
    hx.GP_LOCK.acquire(blocking=True, timeout=2)
    weight = hx.val
    hx.GP_LOCK.release()
    # Get query string
    start_time = int(request.args.get('startTime'))
    if not start_time:
        start_time = round(datetime.datetime.timestamp(datetime.datetime.now()))

    # Query the weight of the food at starting time
    # tables = client_query_api.query(f'from(bucket: "final")\
    #     |> range(start:{start_time}, stop:{start_time + 5000})\
    #     |> filter(fn: (r) => r._measurement == "pet_feeder")\
    # ')

    # Query the weight of the food for now-1m ~ now-30s and now-30s to now
    # If they are the same, write to the database
    tables_previous = client_query_api.query(f'from(bucket: "final")\
            |> range(start:-1m, stop:now())\
            |> filter(fn: (r) => r._measurement == "pet_feeder")\
            |> window(every: 30s)')
    tables_previous = json.dumps(tables_previous, cls=FluxStructureEncoder, indent=2)
    m1 = calc_mean(tables_previous[0])
    m2 = calc_mean(tables_previous[1])
    if abs(m1 - m2) <= 200:
        # write to the database
        return f'{m1} and {m2}'
    return f'{m1} and {m2} is larger than 200'


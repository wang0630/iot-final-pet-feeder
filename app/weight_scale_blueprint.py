from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from flask import Blueprint, jsonify
from hx711py.driver import hx


client = InfluxDBClient(url="http://localhost:8086", token="uw", org="University of Washington")
client_write_api = client.write_api(write_options=SYNCHRONOUS)

weight_scale_blueprint_instance = Blueprint(name='weight_scale', import_name=__name__, url_prefix='/weight')


@weight_scale_blueprint_instance.route('/')
def get_weight():
    hx.GP_LOCK.acquire(blocking=True, timeout=2)
    weight = hx.val
    hx.GP_LOCK.release()
    # Create influxdb data point
    d = {
        "measurement": "pet_feeder",
        "fields": {
            "weight": weight
        },
    }
    p = Point.from_dict(d)
    client_write_api.write(bucket="final", record=p)
    return jsonify(weight=weight)

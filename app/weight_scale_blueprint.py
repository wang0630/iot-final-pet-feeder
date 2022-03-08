from flask import Blueprint
from hx711py.driver import run_hx711
# import influxdb_client
# from influxdb_client.client.write_api import SYNCHRONOUS

weight_scale_blueprint_instance = Blueprint(name='weight_scale', import_name=__name__, url_prefix='/weight')


@weight_scale_blueprint_instance.route('/')
def get_weight():
    weight = run_hx711()
    return f'Weight: {weight}'

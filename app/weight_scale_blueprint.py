from flask import Blueprint
from hx711py.driver import hx
import datetime
# import influxdb_client
# from influxdb_client.client.write_api import SYNCHRONOUS

weight_scale_blueprint_instance = Blueprint(name='weight_scale', import_name=__name__, url_prefix='/weight')


@weight_scale_blueprint_instance.route('/')
def get_weight():
    hx.GP_LOCK.acquire(blocking=True, timeout=2)
    weight = hx.val
    hx.GP_LOCK.release()
    return f'Weight: {weight}'

from flask import Blueprint

weight_scale_blueprint_instance = Blueprint(name='weight_scale', import_name=__name__, url_prefix='/weight')


@weight_scale_blueprint_instance.route('/')
def get_weight():
    return 'get weight'

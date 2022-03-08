# **************************************************************************
# TCSS 573: Internet of Things (IoT)
# The main class to create the Flask app
# **************************************************************************
# Author: Tsung Jui Wang(twang31@uw.edu)
# **************************************************************************
from flask import Flask


def create_app():
    # Create the app
    app = Flask(__name__)

    # Register the route to serve html file
    # Make sure html files are in /templates and css files are in /static
    @app.route("/")
    def test():
        return 'hello'

    # We use app inside distance module, so we need to delay the import to prevent cycle
    from .weight_scale_blueprint import weight_scale_blueprint_instance

    app.register_blueprint(weight_scale_blueprint_instance)
    return app

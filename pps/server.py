import flask
from flask import Flask
# app = Flask(__name__)
LOG = {}

pps_blueprint = flask.Blueprint('pps', __name__)


@pps_blueprint.route('/', methods=["POST"])
def add_new_info():
    payload = flask.request.get_json()
    print(payload)
    if payload and "jobs" in payload:
        for key, value in payload["jobs"].items():
            print(value)
            LOG[key] = value
    else:
        print("No everything is bad")
    return "payload"


@pps_blueprint.route('/', methods=["GET"])
def index():
    print(LOG)
    return flask.render_template('site.html', logs=LOG)


def create_app(*args, **kwargs):
    """Create flask app with all configuration set"""
    app = flask.Flask(__name__)
    app.register_blueprint(pps_blueprint)
    return app


import flask
from flask import Flask
from .enqueuer import resume_job, is_printer_online
from .logger import Logger
from .config import PPS
# app = Flask(__name__)
LOG = {}
my_logger = Logger("Flask")

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


@pps_blueprint.route('/print/', methods=["POST"])
def resume_print():
    if PPS.DRY_RUN:
        return "Dry run"
    job_id = flask.request.form['job_id']
    if not is_printer_online(my_logger):
        return "Print failed. Printer is not online."
    if resume_job(job_id, my_logger):
        LOG[job_id]['status'] = PPS.PRINT_STATUS['DONE']
        return "Print ok"
    else:
        return "Print not ok"


@pps_blueprint.route('/hide/', methods=["POST"])
def hide_row():
    job_id = flask.request.form['job_id']
    if job_id in LOG:
        del LOG[job_id]
        return "Job hidden."
    else:
        return "Job not known."


@pps_blueprint.route('/', methods=["GET"])
def index():
    print(LOG)
    return flask.render_template('site.html', logs=LOG)


def create_app(*args, **kwargs):
    """Create flask app with all configuration set"""
    app = flask.Flask(__name__)
    app.register_blueprint(pps_blueprint)
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    return app


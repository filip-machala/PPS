import flask
from flask import Flask
from .logic import resume_job, is_printer_online
from .logger import Logger
from .config import PPS_CONFIG

pps_blueprint = flask.Blueprint('pps', __name__)


class Server:
    """
    Server class used to store jobs dictionary and logger.
    """
    def __init__(self):
        self.jobs = {}
        self.my_logger = Logger("PPS_Server")

    def get_logger(self) -> Logger:
        return self.my_logger

    def get_jobs(self) -> dict:
        return self.jobs

    def del_job(self, job_id):
        del self.jobs[job_id]

    def set_job_status(self, job_id, status):
        self.jobs[job_id]['status'] = status

    def add_job(self, key, job):
        self.jobs[key] = job


@pps_blueprint.route('/', methods=["POST"])
def add_new_job():
    """
    Add new job to print queue.
    :return: 200 in case of success, 400 in case job wasn't added.
    """
    payload = flask.request.get_json()
    if payload and "jobs" in payload:
        for key, value in payload["jobs"].items():
            flask.current_app.server.add_job(key, value)
    else:
        flask.current_app.server.get_logger().critical("No jobs in post request!")
        return "Bad format of request payload", 400
    return "Jobs added"


@pps_blueprint.route('/print/', methods=["POST"])
def resume_print():
    """
    Resume held job in print queue.
    :return: 200 in case of success otherwise 400
    """
    if PPS_CONFIG.DRY_RUN:
        return "Dry run"
    job_id = flask.request.form['job_id']
    if not is_printer_online(flask.current_app.server.my_logger):
        return "Print failed. Printer is not online.", 200
    if resume_job(job_id, flask.current_app.server.my_logger):
        flask.current_app.server.set_job_status(job_id, PPS_CONFIG.PRINT_STATUS['DONE'])
        return "Print ok"
    else:
        return "Print not ok"


@pps_blueprint.route('/hide/', methods=["POST"])
def hide_row():
    """
    Remove job from jobs dict based on job_id.
    :return: 200 in case of success removal, 400 otherwise.
    """
    job_id = flask.request.form['job_id']
    if job_id in flask.current_app.server.get_jobs():
        flask.current_app.server.del_job(job_id)
        return "Job hidden."
    else:
        return "Job not known."


@pps_blueprint.route('/', methods=["GET"])
def index():
    """
    Render template with actual jobs.
    :return: HTML page.
    """
    return flask.render_template('site.html', logs=flask.current_app.server.get_jobs())


def create_app(*args, **kwargs):
    """
    Create flask app with predefined values.
    :return:
    """
    """Create flask app with all configuration set"""
    app = flask.Flask(__name__)
    app.register_blueprint(pps_blueprint)
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.server = Server()
    return app


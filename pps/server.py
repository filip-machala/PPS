import flask
from flask import Flask, session, request, flash, redirect, url_for
from .logic import resume_job, is_printer_online
from .logger import Logger
from .config import PPS_CONFIG
from .tabledef import *
from sqlalchemy.orm import sessionmaker

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


def logged_id(session) -> bool:
    """
    Check if user is logged_in based on session cookie
    :param session:
    :return: bool True if user is logged in, False otherwise.
    """
    if not session.get('logged_in'):
        return False
    else:
        return True


@pps_blueprint.route('/login/', methods=["GET"])
def login():
    """
    Render template with actual jobs.
    :return: HTML page.
    """
    if not session.get('logged_in'):
        return flask.render_template('login.html')
    else:
        return flask.render_template('site.html', logs=flask.current_app.server.get_jobs())


@pps_blueprint.route('/', methods=["GET"])
def home():
    """
    Render template with actual jobs.
    :return: HTML page.
    """
    if not logged_id(session):
        return flask.redirect("/login/", code=302)
    else:
        return flask.render_template('site.html', logs=flask.current_app.server.get_jobs())


@pps_blueprint.route('/login/', methods=['POST'])
def do_login():
    """
    Login user with values from form as username as password. Then search for user in database.
    :return: Redirects to home page.
    """
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    engine = create_engine('sqlite:///pps.db', echo=True)
    Session = sessionmaker(bind=engine)
    s = Session()
    result = s.query(User).filter_by(username=POST_USERNAME, password=POST_PASSWORD).first()
    if result:
        session['logged_in'] = True
        flask.current_app.server.my_logger.warning("User: " + POST_USERNAME + " successfully logged in.")
    else:
        flask.current_app.server.my_logger.error("User: " + POST_USERNAME + " tried to log in!")
    return flask.redirect("/", code=302)


@pps_blueprint.route('/logout/', methods=['POST'])
def do_logout():
    """
    Logout currently signed in user.
    :return: redirects to home page
    """
    if not logged_id(session):
        return flask.redirect("/login/", code=302)
    else:
        session.pop('logged_in', None)
        return redirect('/')


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
    if not logged_id(session):
        return flask.redirect("/login/", code=302)
    else:
        job_id = flask.request.form['job_id']
        if PPS_CONFIG.DRY_RUN:
            flask.current_app.server.set_job_status(job_id, PPS_CONFIG.PRINT_STATUS['DONE'])
            return "Dry run"
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
    if not logged_id(session):
        return flask.redirect("/login/", code=302)
    else:
        job_id = flask.request.form['job_id']
        if job_id in flask.current_app.server.get_jobs():
            flask.current_app.server.del_job(job_id)
            return "Job hidden."
        else:
            return "Job not known."


def create_app(*args, **kwargs):
    """
    Create flask app with predefined values.
    :return: Flask application
    """
    """Create flask app with all configuration set"""
    app = flask.Flask(__name__)
    app.register_blueprint(pps_blueprint)
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.server = Server()
    app.secret_key = 'No_good_key'
    return app


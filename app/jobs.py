from flask import Blueprint, abort, jsonify

from models.models import Job
from models.database import db_session
from . import func
from . import config as c

app = Blueprint("jobs", __name__, url_prefix="/jobs")


def get_job_from_databese(job_id):
    job = Job.query.filter_by(job_id=job_id).first()
    if not job:
        abort(404, {"code": "Not found", "message": "jobid not found"})
    return job


@app.route("/result/<string:job_id>", methods=["GET"])
def get_result(job_id=None):
    """
    Get result
    """
    job = get_job_from_databese(job_id)

    if job.state == c.done:
        # ToDo
        return jsonify(None)
    else:
        return jsonify({"state": job.state})


@app.route("/result/<string:job_id>", methods=["DELETE"])
@func.header("application/json")
def delete_job(job_id=None):
    job = get_job_from_databese(job_id)

    if job.state == c.done:
        db_session.delete(job)
        db_session.commit()
        # ToDo
        return jsonify(None)
    else:
        return jsonify({"state": job.state})


@app.route("/<string:job_id>", methods=["GET"])
def get_job_state(job_id=None):
    """
    Get job's state.
    """
    job = get_job_from_databese(job_id)
    return jsonify(state=job.state)


@app.route("", methods=["GET"])
def get_jobs():
    """
    Get all registered jobs.
    """
    return jsonify({"jobs": [job.to_dict() for job in Job.query.all()]})


@app.route("/cancel/<string:job_id>", methods=["POST"])
@func.header("application/json")
def cancel_job(job_id=None):
    """
    Cancel a job in the "Waiting" state.
    """
    job = get_job_from_databese(job_id)

    if job.state == func.waiting:
        db_session.delete(job)
        db_session.commit()
        return jsonify({"state": "Canceled"})
    else:
        return jsonify({"state": job.state})

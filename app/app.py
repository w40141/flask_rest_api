import hashlib
import datetime
import functools
from typing import Any

from flask import Flask, abort, jsonify, request, make_response

from models.models import Job
from models.database import db_session

app = Flask(__name__)

waiting = "Waiting"
done = "Done"
running = "Running"
error = "Error"


# check content-type decorator
def content_type(value):
    def _content_type(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not request.headers.get("Content-Type") == value:
                error_message = {"error": "not supported Content-Type"}
                return make_response(jsonify(error_message), 400)

            return func(*args, **kwargs)

        return wrapper

    return _content_type


@app.route("/", methods=["GET"])
def hello():
    """
    Server operation check
    """
    return "I'm working!"


@app.route("/sampler/<string:sampler_name>", methods=["POST"])
@content_type("application/json")
def post_sample(sampler_name=None) -> Any:
    """
    Post matrix to sample
    """
    job_id = make_id(sampler_name)
    job = Job(job_id, sampler_name, waiting, datetime.datetime.now())
    db_session.add(job)
    db_session.commit()
    return jsonify({"job_id": job_id})


def make_id(sampler_name):
    """
    Make job id
    """
    dt_now = datetime.datetime.now()
    job_id = sampler_name + "-" + dt_now.strftime("%Y%m%d%H%M%S%f%f")
    return hashlib.md5(job_id.encode()).hexdigest()


@app.route("/jobs/result/<string:job_id>", methods=["GET"])
def get_result(job_id=None):
    """
    Get result
    """
    job = Job.query.filter_by(job_id=job_id).first()
    if not job:
        abort(404, {"code": "Not found", "message": "jobid not found"})

    if job.state == done:
        # ToDo
        return jsonify(None)
    else:
        return jsonify({"state": job.state})


@app.route("/jobs/delete/<string:job_id>", methods=["DELETE"])
def delete_job(job_id=None):
    job = Job.query.filter_by(job_id=job_id).first()
    if not job:
        abort(404, {"code": "Not found", "message": "jobid not found"})

    if job.state == done:
        db_session.delete(job)
        db_session.commit()
        # ToDo
        return jsonify(None)
    else:
        return jsonify({"state": job.state})


@app.route("/jobs", methods=["GET"])
def get_jobs():
    """
    Get all registered jobs.
    """
    return jsonify({"jobs": [job.to_dict() for job in Job.query.all()]})


@app.route("/jobs/cancel/<string:job_id>", methods=["POST"])
@content_type("application/json")
def cancel_job(job_id=None):
    """
    Cancel a job in the "Waiting" state.
    """
    job = Job.query.filter_by(job_id=job_id).first()
    if not job:
        abort(404, {"code": "Not found", "message": "jobid not found"})

    if job.state == waiting:
        db_session.delete(job)
        db_session.commit()
        return jsonify({"state": "Canceled"})
    else:
        return jsonify({"state": job.state})


@app.errorhandler(400)
@app.errorhandler(404)
def error_handler(error):
    return (
        jsonify(
            {
                "error": {
                    "code": error.description["code"],
                    "message": error.description["message"],
                }
            }
        ),
        error.code,
    )

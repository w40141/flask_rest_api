from flask import Flask, jsonify, abort
from models.models import Job
from models.database import db_session
import datetime
import hashlib

from typing import Any


app = Flask(__name__)

waiting = "Waiting"
done = "Done"
running = "Running"
error = "Error"


@app.route("/", methods=["GET"])
def hello():
    """
    Server operation check
    """
    return "I'm working!"


@app.route("/sampler/<string:sampler_name>", methods=["POST"])
def post_sample(sampler_name=None) -> Any:
    """
    Post matrix to sample
    """
    job_id = make_id(sampler_name)
    state = waiting
    job = Job(job_id, sampler_name, state, datetime.datetime.now())
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
        abort(404, {'code': 'Not found', 'message': 'jobid not found'})
    return jsonify(job.to_dict())


@app.route("/jobs/<string:job_id>", methods=["DELETE"])
def delete_job(job_id=None):
    job = Job.query.filter_by(job_id=job_id).first()
    if not job:
        abort(404, {'code': 'Not found', 'message': 'jobid not found'})

    db_session.delete(job)
    db_session.commit()
    return jsonify(job.to_dict())


@app.route("/jobs", methods=["GET"])
def get_jobs():
    """
    Get all registered jobs.
    """
    return jsonify({'users': [job.to_dict() for job in Job.query.all()]})


@app.route("/jobs/cancel", methods=["POST"])
def cancel_job(job_id=None):
    """
    Cancel a job in the "Waiting" state.
    """
    pass


@app.errorhandler(400)
@app.errorhandler(404)
def error_handler(error):
    # error.code: HTTPステータスコード
    # error.description: abortで設定したdict型
    return jsonify({'error': {
        'code': error.description['code'],
        'message': error.description['message']
    }}), error.code

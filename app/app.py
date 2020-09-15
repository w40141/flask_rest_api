from flask import Flask, jsonify
from models.models import AllJobs
from models.database import db_session
import datetime
import hashlib

from typing import Any


app = Flask(__name__)


@app.route("/", methods=["GET"])
def hello():
    return "I'm working!"


@app.route("/sampler/<string:sampler_name>", methods=["POST"])
def post_sample(sampler_name=None) -> Any:
    """
    -d matrix
    return {'job_id': 'NAME-yyyymmddHHMMSSxxxxxxxx'}
    """
    job_id = make_id(sampler_name)
    job_id = job_id
    sampler = sampler_name
    state = "Waiting"
    alljobs = AllJobs(job_id, sampler, state, datetime.datetime.now())
    db_session.add(alljobs)
    db_session.commit()
    return jsonify({"job_id": job_id})


def make_id(sampler_name):
    dt_now = datetime.datetime.now()
    job_id = sampler_name + "-" + dt_now.strftime("%Y%m%d%H%M%S")
    job_id += hashlib.md5(job_id.encode()).hexdigest()[:4]
    return job_id


@app.route("/jobs/result/<string:job_id>", methods=["GET"])
def get_result(job_id=None):
    job = AllJobs.query.filter_by(job_id=job_id).first()
    return jsonify(job.to_dict())


@app.route("/jobs/result/<string:job_id>", methods=["DELETE"])
def delete_result(job_id=None):
    pass


@app.route("/jobs", methods=["GET"])
def get_jobs():
    return jsonify({'users': [job.to_dict() for job in AllJobs.query.all()]})


@app.route("/jobs", methods=["POST"])
def cansel_job(job_id=None):
    pass


if __name__ == "__main__":
    app.run(port=5000, debug=True)

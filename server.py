from flask import Flask
import datetime
import hashlib

from typing import Dict


app = Flask(__name__)


@app.route("/", methods=["GET"])
def hello():
    return "I'm working!"


@app.route("/sampler/<string:sampler_name>", methods=['POST'])
def post_sample(sampler_name=None) -> Dict[str, str]:
    """
    -d matrix
    return {'job_id': 'NAME-yyyymmddHHMMSSxxxxxxxx'}
    """
    job_id = make_id(sampler_name)
    return {'job_id': job_id}


def make_id(sampler_name):
    dt_now = datetime.datetime.now()
    job_id = sampler_name + '-' + dt_now.strftime('%Y%m%d%H%M%S')
    job_id += hashlib.md5(job_id.encode()).hexdigest()[:4]
    return job_id


@app.route("/jobs/<string:job_id>", methods=['GET'])
def get_result(job_id=None):
    pass


if __name__ == "__main__":
    app.run(port=5000, debug=True)

from flask import Flask
from sampler import sample

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
    return sample(sampler_name)


@app.route("/jobs/<string:job_id>", methods=['GET'])
def get_result(job_id=None):
    return 

if __name__ == "__main__":
    app.run(port=5000, debug=True)

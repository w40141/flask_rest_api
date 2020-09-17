from flask import Flask, jsonify
from . import jobs
from . import sampler

# from models.models import Job

app = Flask(__name__)
app.register_blueprint(jobs.app)
app.register_blueprint(sampler.app)


@app.route("/", methods=["GET"])
def hello():
    """
    Server operation check
    """
    return "I'm working!"


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

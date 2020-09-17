import os
import datetime

from flask import Blueprint, flash, jsonify, request, redirect

from . import func
from . import config as c
from models.models import Job
from models.database import db_session

app = Blueprint("sampler", __name__, url_prefix="/sampler")


@app.route("/<string:sampler_name>", methods=["POST"])
@func.header("application/json")
def post_sample(sampler_name=None):
    """
    Post matrix to sample
    """
    job_id = func.make_id(sampler_name)
    job = Job(
        job_id=job_id, sampler=sampler_name, state=c.waiting, date=datetime.datetime.now()
    )
    db_session.add(job)
    db_session.commit()
    return jsonify(dict(job_id=job_id))


@app.route("/uploads/<string:sampler_name>", methods=["POST"])
@func.header("application/json")
def upload_file(sampler_name):
    # check if the post request has the file part
    if "file" not in request.files:
        flash("No file part")
        return redirect(request.url)
    file = request.files["file"]
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == "":
        flash("No selected file")
        return redirect(request.url)
    if file and func.allowed_file(file.filename):
        job_id = func.make_id(sampler_name)
        file.save(os.path.join(c.UPLOAD_FOLDER, job_id))
        return jsonify(dict(job_id=job_id))

import hashlib
import datetime

import functools
from flask import request, jsonify, make_response

from . import config as c


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in c.ALLOWED_EXTENSIONS


# check header decorator
def header(value):
    def _header(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not request.headers.get("Accept") == value:
                error_message = {"error": "not supported Accept"}
                return make_response(jsonify(error_message), 400)

            if not request.headers.get("Content-Type") == value:
                error_message = {"error": "not supported Content-Type"}
                return make_response(jsonify(error_message), 400)

            return func(*args, **kwargs)

        return wrapper

    return _header


def make_id(sampler_name):
    """
    Make job id
    """
    dt_now = datetime.datetime.now()
    job_id = sampler_name + "-" + dt_now.strftime("%Y%m%d%H%M%S%f%f")
    return hashlib.md5(job_id.encode()).hexdigest()

from flask import Blueprint


app = Blueprint('test', __name__)


@app.route('/sample')
def test():
    return 'test'

from flask import Flask
from flask_restful import Api, Resource, abort, reqparse


app = Flask(__name__)
api = Api(app)


class Hello(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", required=True, help="Name cannot be blank!")
        parser.add_argument("age", type=int, help="Age cannot be converted")
        args = parser.parse_args()
        if not args["name"]:
            abort(401, message={"name": "Name cannot be blank! 2"})
        return {"name": "Hello {}!".format(args["name"]), "age": args["age"]}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "q_param", type=int, location="args", help="q_param is numbers"
        )
        parser.add_argument("f_param", location="form")
        args = parser.parse_args()
        return {
            "post": "Hello World!",
            "qParam": args["q_param"],
            "fParam": args["f_param"],
        }


api.add_resource(Hello, "/")


if __name__ == "__main__":
    app.run(port=5000, debug=True)

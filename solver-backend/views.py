import flask
from flask_cors import CORS

main = flask.Blueprint('main', __name__)
cors = CORS(main, resources={r"/api/*": {"origins": "*"}})


@main.route("/api/image/", methods=["POST"])
def process_image():
    picture = flask.request.json
    return picture["image"]


@main.route("/api/solve/", methods=["POST"])
def solve():
    board = flask.request.json
    return "recieved"

import flask
from flask_cors import CORS
from image_processing.process import process

main = flask.Blueprint('main', __name__)
cors = CORS(main, resources={r"/api/*": {"origins": "*"}})


@main.route("/api/image/", methods=["POST"])
def process_image():
    picture = flask.request.json
    board = process(picture["image"])
    return board


@main.route("/api/solve/", methods=["POST"])
def solve():
    board = flask.request.json
    return "recieved"

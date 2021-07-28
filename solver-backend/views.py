import flask
from flask_cors import CORS

main = flask.Blueprint('main', __name__)
cors = CORS(main, resources={r"/api/*": {"origins": "*"}})


@main.route('/')
def main_index():
    return "Hello World"


@main.route("/api/image/", methods=["GET", "POST"])
def process_image():
    picture = flask.request.json
    return picture["image"]

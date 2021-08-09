import flask
from flask_cors import CORS

from views import *

app = flask.Flask(__name__)


def create_app(config_file="settings.py"):
    app = flask.Flask(__name__)

    app.config.from_pyfile(config_file)

    app.register_blueprint(main)

    return app


if __name__ == '__main__':
    app.run(threaded=True, port=5000)

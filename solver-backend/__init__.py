import flask
from flask_cors import CORS

# from .extensions import X
from .views import main


def create_app(config_file="settings.py"):
    app = flask.Flask(__name__)

    app.config.from_pyfile(config_file)

    app.register_blueprint(main)

    return app

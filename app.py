import cv2
from views import *


def create_app():
    app = flask.Flask(__name__)
    app.register_blueprint(main)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(threaded=True, host="0.0.0.0", port=3001)

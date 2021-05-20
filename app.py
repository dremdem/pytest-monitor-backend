"""Main application module"""

import flask
import api


def create_app():
    app = flask.Flask(__name__)
    api.api.init_app(app)

    @app.route('/')
    def hello_world():
        return 'pytest-monitor-backend'

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', debug=True)

import os
import traceback
from flask import Flask
from flask_cors import CORS
from sqlalchemy import exc

from models.database import setup_db
from routes.health import health_blueprint


def create_app():
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    app.register_blueprint(health_blueprint)

    return app


app = create_app()

if __name__ == '__main__':
    app.run()

import os
import traceback
from flask import Flask
from flask_cors import CORS

from util import get_database_url
from models.database import db, migrate
from models.casting import Actor, Movie, actor_movie_relation
from routes import health_blueprint, casting_blueprint
from errors import errors_blueprint

def create_app(database_url):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    app.register_blueprint(health_blueprint)
    app.register_blueprint(casting_blueprint)
    app.register_blueprint(errors_blueprint)
    return app


database_url = get_database_url()
app = create_app(database_url)

if __name__ == '__main__':
    app.run()

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from util import get_database_url

database_url = get_database_url()
db = SQLAlchemy()


def setup_db(app, database_url=database_url):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    migrate = Migrate(app, db)

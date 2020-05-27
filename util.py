import os
from dotenv import load_dotenv
from flask import request
from werkzeug.exceptions import BadRequest


load_dotenv()
db_config = {
    'user': os.getenv('DB_USER', 'casting_api'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'casting')
}


def create_database_url(user, password, host, database):
    url = 'postgresql://{}:{}@{}/{}'.\
        format(
            user,
            password,
            host,
            database)

    return url

def get_database_url(db_name=None):
    db_url = os.getenv('DATABASE_URL')
    if db_url:
        return db_url

    if not db_config['password']:
        message = (
            'System Exit:'
            ' The database password was not found'
            ' in the "DB_PASSWORD" env variable.')
        raise SystemExit(message)

    if db_name:
        db_config['database'] = db_name

    db_url = create_database_url(**db_config)
    return db_url


def load_data(schema, partial=False):
    if not request.data:
        raise BadRequest(
            description='The request did not contain a request body.'
        )

    if not request.is_json:
        raise BadRequest(
            description='The request expected a JSON request body.'
        )

    data = schema.load(
        request.get_json(),
        partial=partial
    )

    return data

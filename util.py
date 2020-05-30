import os
from pathlib import Path
from dotenv import load_dotenv
from flask import request
from werkzeug.exceptions import BadRequest
from datetime import datetime
from models.database import db


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


def load_test_env():
    env_path = str(Path('.env-test').absolute())
    load_dotenv(env_path)


def set_auth_token(client, token):
    client.environ_base['HTTP_AUTHORIZATION'] = f'Bearer {token}'


mock_data = {
    'actor_a': {
        'name': 'Tom Hanks',
        'age': 64,
        'gender': 'male'
    },
    'movie_a': {
        'title': 'Forrest Gump',
        'release_date': datetime.fromisoformat('1994-07-06T00:00:00')
    },
    'actor_b': {
        'name': 'Al Pacino',
        'age': 80,
        'gender': 'male'
    },
    'actors_b': [
        {
            'name': 'Robert Duvall',
            'age': 89,
            'gender': 'male'
        },
        {
            'name': 'Diane Keaton',
            'age': 74,
            'gender': 'female'
        }
    ],
    'movies_b': [
        {
            'title': 'The Godfather',
            'release_date': datetime.fromisoformat('1972-03-24T00:00:00')
        },
        {
            'title': 'The Godfather: Part II',
            'release_date': datetime.fromisoformat('1974-12-18T00:00:00')
        }
    ]
}

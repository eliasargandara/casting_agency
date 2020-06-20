import os
from unittest import TestCase, main

from app import create_app
from models.database import db
from models.casting import Actor, Movie
from util import get_database_url, load_test_env, set_auth_token, mock_data


load_test_env()

ASSISTANT_TOKEN = os.getenv('ASSISTANT_TOKEN')
DIRECTOR_TOKEN = os.getenv('DIRECTOR_TOKEN')
EXECUTIVE_TOKEN = os.getenv('EXECUTIVE_TOKEN')

class DeleteMovieTestCase(TestCase):
    def setUp(self):
        self.db_name = 'casting_test'
        self.app = create_app(get_database_url(self.db_name))
        self.client = self.app.test_client()

        with self.app.app_context():
            self.db = db
            self.db.drop_all()
            self.db.create_all()

    def tearDown(self):
        with self.app.app_context():
            self.db.drop_all()

    def test_delete_movie_when_requested_by_assistant(self):
        set_auth_token(self.client, ASSISTANT_TOKEN)

        movie_id = None
        expected = None
        with self.app.app_context():
            mock_movie = mock_data['movie_a']
            movie = Movie(**mock_movie)
            movie.insert()

            movie_id = movie.id
            expected = {
                'success': False,
                'description': (
                    'The account is not authorized to access this resource.')
            }

        response = self.client.delete(f'/movies/{movie_id}')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = response.get_json()
        self.assertEqual(data, expected)

    def test_delete_movie_when_requested_by_director(self):
        set_auth_token(self.client, DIRECTOR_TOKEN)

        movie_id = None
        expected = None
        with self.app.app_context():
            mock_movie = mock_data['movie_a']
            movie = Movie(**mock_movie)
            movie.insert()

            movie_id = movie.id
            expected = {
                'success': False,
                'description': (
                    'The account is not authorized to access this resource.')
            }

        response = self.client.delete(f'/movies/{movie_id}')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = response.get_json()
        self.assertEqual(data, expected)

    def test_delete_movie_when_requested_by_executive(self):
        set_auth_token(self.client, EXECUTIVE_TOKEN)

        movie_id = None
        expected = None
        with self.app.app_context():
            mock_movie = mock_data['movie_a']
            movie = Movie(**mock_movie)
            movie.insert()
            movie_id = movie.id

            expected = {
                'success': True,
                'id': movie_id
            }

        response = self.client.delete(f'/movies/{movie_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = response.get_json()
        self.assertEqual(data, expected)

    def test_delete_movie_when_requested_without_token(self):
        movie_id = None
        expected = None
        with self.app.app_context():
            mock_movie = mock_data['movie_a']
            movie = Movie(**mock_movie)
            movie.insert()

            movie_id = movie.id
            expected = {
                'success': False,
                'description': 'Authorization header is expected.'
            }

        response = self.client.delete(f'/movies/{movie_id}')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = response.get_json()
        self.assertEqual(data, expected)

    def test_delete_movie_when_movie_not_found(self):
        movie_id = 1
        expected = {
            'success': False,
            'description': (
                'The requested URL was not found on the server. If you entered'
                ' the URL manually please check your spelling and try again.'
            )
        }

        response = self.client.delete(f'/movies{movie_id}')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = response.get_json()
        self.assertEqual(data, expected)


if __name__ == '__main__':
    main()

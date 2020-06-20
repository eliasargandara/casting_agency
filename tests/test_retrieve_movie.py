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

class RetrieveMovieTestCase(TestCase):
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

    def test_retrieve_movies_when_requested_by_assistant(self):
        set_auth_token(self.client, ASSISTANT_TOKEN)

        expected = None
        with self.app.app_context():
            mock_movie = mock_data['movie_a']
            movie = Movie(**mock_movie)
            movie.insert()

            release_date = mock_movie['release_date'].isoformat()
            expected_movies = [{
                'id': movie.id,
                **mock_data['movie_a'],
                'release_date': release_date,
                'actors': []
            }]

            expected = {
                'success': True,
                'data': expected_movies
            }

        response = self.client.get('/movies')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = response.get_json()
        self.assertEqual(data, expected)

    def test_retrieve_movies_when_requested_by_director(self):
        set_auth_token(self.client, DIRECTOR_TOKEN)

        expected = None
        with self.app.app_context():
            mock_movie = mock_data['movie_a']
            movie = Movie(**mock_movie)
            movie.insert()

            release_date = mock_movie['release_date'].isoformat()
            expected_movies = [{
                'id': movie.id,
                **mock_data['movie_a'],
                'release_date': release_date,
                'actors': []
            }]

            expected = {
                'success': True,
                'data': expected_movies
            }

        response = self.client.get('/movies')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = response.get_json()
        self.assertEqual(data, expected)

    def test_retrieve_movies_when_requested_by_executive(self):
        set_auth_token(self.client, EXECUTIVE_TOKEN)

        expected = None
        with self.app.app_context():
            mock_movie = mock_data['movie_a']
            movie = Movie(**mock_movie)
            movie.insert()

            release_date = mock_movie['release_date'].isoformat()
            expected_movies = [{
                'id': movie.id,
                **mock_data['movie_a'],
                'release_date': release_date,
                'actors': []
            }]

            expected = {
                'success': True,
                'data': expected_movies
            }

        response = self.client.get('/movies')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = response.get_json()
        self.assertEqual(data, expected)

    def test_retrieve_movies_when_requested_without_token(self):
        expected = {
            'success': False,
            'description': 'Authorization header is expected.'
        }

        response = self.client.get('/movies')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = response.get_json()
        self.assertEqual(data, expected)

    def test_retrieve_movies_when_no_movies_exist(self):
        set_auth_token(self.client, ASSISTANT_TOKEN)

        expected = {
            'success': True,
            'data': []
        }

        response = self.client.get('/movies')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = response.get_json()
        self.assertEqual(data, expected)

    def test_retrieve_movies_when_multiple_movies_exist(self):
        set_auth_token(self.client, ASSISTANT_TOKEN)

        expected = None
        with self.app.app_context():
            expected_movies = []
            for mock_movie in mock_data['movies_b']:
                movie = Movie(**mock_movie)
                movie.insert()

                release_date = mock_movie['release_date'].isoformat()
                expected_movies.append({
                    'id': movie.id,
                    **mock_movie,
                    'release_date': release_date,
                    'actors': []
                })

            expected = {
                'success': True,
                'data': expected_movies
            }

        response = self.client.get('/movies')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = response.get_json()
        self.assertEqual(data, expected)

    def test_retrieve_movies_when_movie_has_movies(self):
        set_auth_token(self.client, ASSISTANT_TOKEN)

        expected = None
        with self.app.app_context():
            mock_movie = mock_data['movie_a']
            mock_actor = mock_data['actor_a']

            movie = Movie(**mock_movie)
            actor = Actor(**mock_actor)
            movie.actors = [actor]
            movie.insert()

            expected_actors = [{
                'id': actor.id,
                **mock_actor
            }]

            release_date = mock_movie['release_date'].isoformat()
            expected_movies = [{
                'id': movie.id,
                **mock_movie,
                'release_date': release_date,
                'actors': expected_actors
            }]

            expected = {
                'success': True,
                'data': expected_movies
            }

        response = self.client.get('/movies')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = response.get_json()
        self.assertEqual(data, expected)


if __name__ == '__main__':
    main()

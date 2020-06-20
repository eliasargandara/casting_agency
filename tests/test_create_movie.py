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

class CreateMovieTestCase(TestCase):
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

    def test_create_movie_when_requested_by_assistant(self):
        set_auth_token(self.client, ASSISTANT_TOKEN)

        mock_movie = mock_data['movie_a']
        payload = {
            **mock_movie
        }

        expected = {
            'success': False,
            'description': (
                'The account is not authorized to access this resource.'
            )
        }

        response = self.client.post('/movies', json=payload)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = response.get_json()
        self.assertEqual(data, expected)

    def test_create_movie_when_requested_by_director(self):
        set_auth_token(self.client, DIRECTOR_TOKEN)

        mock_movie = mock_data['movie_a']
        payload = {
            **mock_movie
        }

        expected = {
            'success': False,
            'description': (
                'The account is not authorized to access this resource.'
            )
        }

        response = self.client.post('/movies', json=payload)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = response.get_json()
        self.assertEqual(data, expected)

    def test_create_movie_when_requested_by_executive(self):
        set_auth_token(self.client, EXECUTIVE_TOKEN)

        mock_movie = mock_data['movie_a']
        release_date = mock_movie['release_date'].isoformat()
        payload = {
            **mock_movie,
            'release_date': release_date
        }

        expected_movies = [{
            **mock_movie,
            'actors': [],
            'release_date': release_date
        }]

        expected = {
            'success': True,
            'data': expected_movies
        }

        response = self.client.post('/movies', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = response.get_json()
        for movie in data['data']:
            self.assertTrue(movie.pop('id'))

        self.assertEqual(data, expected)

    def test_create_movie_when_requested_without_token(self):
        mock_movie = mock_data['movie_a']
        payload = {
            **mock_movie
        }

        expected = {
            'success': False,
            'description': 'Authorization header is expected.'
        }

        response = self.client.post('/actors', json=payload)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = response.get_json()
        self.assertEqual(data, expected)

    def test_create_movie_when_movie_has_movies(self):
        set_auth_token(self.client, EXECUTIVE_TOKEN)

        payload = None
        expected = None
        with self.app.app_context():
            actor_ids = []
            expected_actors = []
            mock_actors = mock_data['actors_b']
            for mock_actor in mock_actors:
                actor = Actor(**mock_actor)
                actor.insert()

                actor_ids.append(actor.id)
                expected_actors.append({
                    'id': actor.id,
                    **mock_actor
                })

            mock_movie = mock_data['movies_b'][1]
            release_date = mock_movie['release_date'].isoformat()
            payload = {
                **mock_movie,
                'release_date': release_date,
                'actors': actor_ids
            }

            expected_movies = [{
                **mock_movie,
                'release_date': release_date,
                'actors': expected_actors
            }]

            expected = {
                'success': True,
                'data': expected_movies
            }

        response = self.client.post('/movies', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = response.get_json()
        for movie in data['data']:
            self.assertTrue(movie.pop('id'))

        self.assertEqual(data, expected)

    def test_create_movie_when_one_required_argument_missing(self):
        set_auth_token(self.client, EXECUTIVE_TOKEN)

        mock_movie = mock_data['movie_a']
        payload = {**mock_movie}
        del payload['release_date']

        expected = {
            'success': False,
            'description': 'The request parameters are not valid.',
            'invalid_params': [{
                'name': 'release_date',
                'reason': 'Missing data for required field.'
            }]
        }

        response = self.client.post('/movies', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = response.get_json()
        self.assertEqual(data, expected)

    def test_create_movie_when_many_required_arguments_missing(self):
        set_auth_token(self.client, EXECUTIVE_TOKEN)

        mock_movie = mock_data['movie_a']
        payload = {}

        expected = {
            'success': False,
            'description': 'The request parameters are not valid.',
            'invalid_params': [
                {
                    'name': 'title',
                    'reason': 'Missing data for required field.'
                },
                {
                    'name': 'release_date',
                    'reason': 'Missing data for required field.'
                }
            ]
        }

        response = self.client.post('/movies', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = response.get_json()
        self.assertEqual(data, expected)

    def test_create_movie_when_unkown_argument_provided(self):
        set_auth_token(self.client, EXECUTIVE_TOKEN)

        mock_movie = mock_data['movie_a']
        release_date = mock_movie['release_date'].isoformat()
        payload = {
            **mock_movie,
            'release_date': release_date,
            'genre': 'Action'
        }

        expected = {
            'success': False,
            'description': 'The request parameters are not valid.',
            'invalid_params': [{
                'name': 'genre',
                'reason': 'Unknown field.'
            }]
        }

        response = self.client.post('/movies', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = response.get_json()
        self.assertEqual(data, expected)


if __name__ == '__main__':
    main()

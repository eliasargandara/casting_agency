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

class CreateActorTestCase(TestCase):
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

    def test_create_actor_when_requested_by_assistant(self):
        set_auth_token(self.client, ASSISTANT_TOKEN)

        mock_actor = mock_data['actor_a']
        payload = {
            **mock_actor
        }

        expected = {
            'success': False,
            'description': (
                'The account is not authorized to access this resource.')
        }

        response = self.client.post('/actors', json=payload)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = response.get_json()
        self.assertEqual(data, expected)

    def test_create_actor_when_requested_by_director(self):
        set_auth_token(self.client, DIRECTOR_TOKEN)

        mock_actor = mock_data['actor_a']
        payload = {
            **mock_actor
        }

        expected_actors = [{
            **mock_actor,
            'movies': []
        }]

        expected = {
            'success': True,
            'data': expected_actors
        }

        response = self.client.post('/actors', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = response.get_json()
        for actor in data['data']:
            self.assertTrue(actor.pop('id'))

        self.assertEqual(data, expected)

    def test_create_actor_when_requested_by_executive(self):
        set_auth_token(self.client, EXECUTIVE_TOKEN)

        mock_actor = mock_data['actor_a']
        payload = {
            **mock_actor
        }

        expected_actors = [{
            **mock_actor,
            'movies': []
        }]

        expected = {
            'success': True,
            'data': expected_actors
        }

        response = self.client.post('/actors', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = response.get_json()
        for actor in data['data']:
            self.assertTrue(actor.pop('id'))

        self.assertEqual(data, expected)

    def test_create_actor_when_requested_without_token(self):
        mock_actor = mock_data['actor_a']

        payload = {
            **mock_actor
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

    def test_create_actor_when_actor_has_no_movies_exist(self):
        set_auth_token(self.client, DIRECTOR_TOKEN)

        mock_actor = mock_data['actor_a']
        payload = {
            **mock_actor
        }

        expected_actors = [{
            **mock_actor,
            'movies': []
        }]

        expected = {
            'success': True,
            'data': expected_actors
        }

        response = self.client.post('/actors', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = response.get_json()
        for actor in data['data']:
            self.assertTrue(actor.pop('id'))

        self.assertEqual(data, expected)

    def test_create_actor_when_actor_has_multiple_movies(self):
        set_auth_token(self.client, DIRECTOR_TOKEN)

        payload = None
        expected = None
        with self.app.app_context():
            movie_ids = []
            expected_movies = []
            mock_movies = mock_data['movies_b']
            for mock_movie in mock_movies:
                movie = Movie(**mock_movie)
                movie.insert()

                movie_ids.append(movie.id)
                release_date = mock_movie['release_date'].isoformat()
                expected_movies.append({
                    'id': movie.id,
                    **mock_movie,
                    'release_date': release_date
                })

            mock_actor = mock_data['actor_b']
            payload = {
                **mock_actor,
                'movies': movie_ids
            }

            expected_actors = [{
                **mock_actor,
                'movies': expected_movies
            }]

            expected = {
                'success': True,
                'data': expected_actors
            }

        response = self.client.post('/actors', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = response.get_json()
        for actor in data['data']:
            self.assertTrue(actor.pop('id'))

        self.assertEqual(data, expected)

    def test_create_actor_when_one_required_argument_missing(self):
        set_auth_token(self.client, DIRECTOR_TOKEN)

        mock_actor = mock_data['actor_a']
        payload = {**mock_actor}
        del payload['name']

        expected = {
            'success': False,
            'description': 'The request parameters are not valid.',
            'invalid_params': [{
                'name': 'name',
                'reason': 'Missing data for required field.'
            }]
        }

        response = self.client.post('/actors', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = response.get_json()
        self.assertEqual(data, expected)

    def test_create_actor_when_many_required_arguments_missing(self):
        set_auth_token(self.client, DIRECTOR_TOKEN)

        mock_actor = mock_data['actor_a']
        payload = {'name': mock_actor['name']}

        invalid_params = [
            {
                'name': 'age',
                'reason': 'Missing data for required field.'
            },
            {
                'name': 'gender',
                'reason': 'Missing data for required field.'
            }
        ]

        expected = {
            'success': False,
            'description': 'The request parameters are not valid.',
            'invalid_params': invalid_params
        }

        response = self.client.post('/actors', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = response.get_json()
        self.assertEqual(data, expected)

    def test_create_actor_when_unkown_argument_provided(self):
        set_auth_token(self.client, DIRECTOR_TOKEN)

        mock_actor = mock_data['actor_a']
        payload = {
            **mock_actor,
            'username': mock_actor['name']
        }

        expected = {
            'success': False,
            'description': 'The request parameters are not valid.',
            'invalid_params': [{
                'name': 'username',
                'reason': 'Unknown field.'
            }]
        }

        response = self.client.post('/actors', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = response.get_json()
        self.assertEqual(data, expected)

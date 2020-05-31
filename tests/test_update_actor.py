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

class UpdateActorTestCase(TestCase):
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

    def test_update_actor_when_requested_by_assistant(self):
        set_auth_token(self.client, ASSISTANT_TOKEN)

        actor_id = None
        expected = None
        payload = None
        with self.app.app_context():
            mock_actor = mock_data['actor_a']
            actor = Actor(**mock_actor)
            actor.insert()

            age = mock_actor['age'] + 1
            payload = {
                'age': age
            }

            actor_id = actor.id
            expected = {
                'success': False,
                'description': (
                    'The account is not authorized to access this resource.')
            }

        response = self.client.patch(f'/actors/{actor_id}', json=payload)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = response.get_json()
        self.assertEqual(data, expected)

    def test_update_actor_when_requested_by_director(self):
        set_auth_token(self.client, DIRECTOR_TOKEN)

        actor_id = None
        payload = None
        expected = None
        with self.app.app_context():
            mock_actor = mock_data['actor_a']
            actor = Actor(**mock_actor)
            actor.insert()

            age = mock_actor['age'] + 1
            payload = {
                'age': age
            }

            actor_id = actor.id
            expected_actors = [{
                'id': actor_id,
                **mock_actor,
                'age': age,
                'movies': []
            }]

            expected = {
                'success': True,
                'data': expected_actors
            }

        response = self.client.patch(f'/actors/{actor_id}', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = response.get_json()
        self.assertEqual(data, expected)

    def test_update_actor_when_requested_by_executive(self):
        set_auth_token(self.client, EXECUTIVE_TOKEN)

        actor_id = None
        payload = None
        expected = None
        with self.app.app_context():
            mock_actor = mock_data['actor_a']
            actor = Actor(**mock_actor)
            actor.insert()

            age = mock_actor['age'] + 1
            payload = {
                'age': age
            }

            actor_id = actor.id
            expected_actors = [{
                'id': actor_id,
                **mock_actor,
                'age': age,
                'movies': []
            }]

            expected = {
                'success': True,
                'data': expected_actors
            }

        response = self.client.patch(f'/actors/{actor_id}', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = response.get_json()
        self.assertEqual(data, expected)

    def test_update_actor_when_requested_without_token(self):
        actor_id = None
        expected = None
        payload = None
        with self.app.app_context():
            mock_actor = mock_data['actor_a']
            actor = Actor(**mock_actor)
            actor.insert()

            age = mock_actor['age'] + 1
            payload = {
                'age': age
            }

            actor_id = actor.id
            expected = {
                'success': False,
                'description': 'Authorization header is expected.'
            }

        response = self.client.patch(f'/actors/{actor_id}', json=payload)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = response.get_json()
        self.assertEqual(data, expected)

    def test_update_actor_movies_when_actor_has_no_movies(self):
        set_auth_token(self.client, DIRECTOR_TOKEN)

        payload = None
        actor_id = None
        payload = None
        with self.app.app_context():
            mock_actor = mock_data['actor_a']
            mock_movie = mock_data['movie_a']

            actor = Actor(**mock_actor)
            actor.insert()

            movie = Movie(**mock_movie)
            movie.insert()

            payload = {
                'movies': [movie.id]
            }

            actor_id = actor.id
            release_date = mock_movie['release_date'].isoformat()
            expected_actors = [{
                'id': actor_id,
                **mock_actor,
                'movies': [{
                    'id': movie.id,
                    **mock_movie,
                    'release_date': release_date
                }]
            }]

            expected = {
                'success': True,
                'data': expected_actors
            }

        response = self.client.patch(f'/actors/{actor_id}', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = response.get_json()
        self.assertEqual(data, expected)

    def test_update_actor_movies_when_actor_has_movies(self):
        set_auth_token(self.client, DIRECTOR_TOKEN)

        payload = {'movies': []}
        actor_id = None
        expected = None
        with self.app.app_context():
            mock_actor_movies = mock_data['movies_b']
            expected_movies = []
            movies = []
            for mock_movie in mock_actor_movies:
                movie = Movie(**mock_movie)
                movie.insert()
                movies.append(movie)

                payload['movies'].append(movie.id)

                release_date = mock_movie['release_date'].isoformat()
                expected_movies.append({
                    'id': movie.id,
                    **mock_movie,
                    'release_date': release_date
                })

            payload['movies'].pop()
            expected_movies.pop()

            mock_actor = mock_data['actor_b']
            actor = Actor(**mock_actor)
            actor.movies = movies
            actor.insert()
            actor_id = actor.id

            expected_actors = [{
                'id': actor_id,
                **mock_actor,
                'movies': expected_movies
            }]

            expected = {
                'success': True,
                'data': expected_actors
            }

        response = self.client.patch(f'/actors/{actor_id}', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = response.get_json()
        self.assertEqual(data, expected)

    def test_update_actor_when_unkown_argument_provided(self):
        set_auth_token(self.client, DIRECTOR_TOKEN)

        payload = None
        actor_id = None
        expected = None
        with self.app.app_context():
            mock_actor = mock_data['actor_a']
            actor = Actor(**mock_actor)
            actor.insert()
            actor_id = actor.id

            payload = {'nickname': 'Johnny'}

            expected = {
                'success': False,
                'description': 'The request parameters are not valid.',
                'invalid_params': [{
                    'name': 'nickname',
                    'reason': 'Unknown field.'
                }]
            }

        response = self.client.patch(f'/actors/{actor_id}', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = response.get_json()
        self.assertEqual(data, expected)

    def test_update_actor_when_actor_not_found(self):
        set_auth_token(self.client, DIRECTOR_TOKEN)

        actor_id = 24
        payload = {}
        expected = {
            'success': False,
            'description': 'An actor with the id "24" was not found.',
        }

        response = self.client.patch(f'/actors/{actor_id}', json=payload)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = response.get_json()
        self.assertEqual(data, expected)

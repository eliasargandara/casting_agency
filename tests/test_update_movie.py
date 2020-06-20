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

class UpdateMovieTestCase(TestCase):
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

    def test_update_movie_when_requested_by_assistant(self):
        set_auth_token(self.client, ASSISTANT_TOKEN)

        movie_id = None
        expected = None
        payload = None
        with self.app.app_context():
            mock_movie = mock_data['movie_a']
            movie = Movie(**mock_movie)
            movie.insert()

            title = 'New Movie Title'
            payload = {
                'title': title
            }

            movie_id = movie.id
            expected = {
                'success': False,
                'description': (
                    'The account is not authorized to access this resource.'
                )
            }

        response = self.client.patch(f'/movies/{movie_id}', json=payload)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = response.get_json()
        self.assertEqual(data, expected)

    def test_update_movie_when_requested_by_director(self):
        set_auth_token(self.client, DIRECTOR_TOKEN)

        movie_id = None
        payload = None
        expected = None
        with self.app.app_context():
            mock_movie = mock_data['movie_a']
            movie = Movie(**mock_movie)
            movie.insert()

            title = 'New Movie Title'
            payload = {
                'title': title
            }

            movie_id = movie.id
            release_date = mock_movie['release_date'].isoformat()
            expected_movies = [{
                'id': movie_id,
                **mock_movie,
                'release_date': release_date,
                'title': title,
                'actors': []
            }]

            expected = {
                'success': True,
                'data': expected_movies
            }

        response = self.client.patch(f'/movies/{movie_id}', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = response.get_json()
        self.assertEqual(data, expected)

    def test_update_movie_when_requested_by_executive(self):
        set_auth_token(self.client, EXECUTIVE_TOKEN)

        movie_id = None
        payload = None
        expected = None
        with self.app.app_context():
            mock_movie = mock_data['movie_a']
            movie = Movie(**mock_movie)
            movie.insert()

            title = 'New Movie Title'
            payload = {
                'title': title
            }

            movie_id = movie.id
            release_date = mock_movie['release_date'].isoformat()
            expected_movies = [{
                'id': movie_id,
                **mock_movie,
                'release_date': release_date,
                'title': title,
                'actors': []
            }]

            expected = {
                'success': True,
                'data': expected_movies
            }

        response = self.client.patch(f'/movies/{movie_id}', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = response.get_json()
        self.assertEqual(data, expected)

    def test_update_movie_when_requested_without_token(self):
        movie_id = None
        expected = None
        payload = None
        with self.app.app_context():
            mock_movie = mock_data['movie_a']
            movie = Movie(**mock_movie)
            movie.insert()

            title = 'New Movie Title'
            payload = {
                'title': title
            }

            movie_id = movie.id
            expected = {
                'success': False,
                'description': 'Authorization header is expected.'
            }

        response = self.client.patch(f'/movies/{movie_id}', json=payload)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = response.get_json()
        self.assertEqual(data, expected)

    def test_update_movie_movies_when_movie_has_no_movies(self):
        set_auth_token(self.client, DIRECTOR_TOKEN)

        payload = None
        movie_id = None
        payload = None
        with self.app.app_context():
            mock_actor = mock_data['actor_a']
            mock_movie = mock_data['movie_a']

            actor = Actor(**mock_actor)
            actor.insert()

            movie = Movie(**mock_movie)
            movie.insert()

            payload = {
                'actors': [actor.id]
            }

            movie_id = movie.id
            release_date = mock_movie['release_date'].isoformat()
            expected_movies = [{
                'id': movie.id,
                **mock_movie,
                'release_date': release_date,
                'actors': [{
                    'id': actor.id,
                    **mock_actor,
                }]
            }]

            expected = {
                'success': True,
                'data': expected_movies
            }

        response = self.client.patch(f'/movies/{movie_id}', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = response.get_json()
        self.assertEqual(data, expected)

    def test_update_movie_movies_when_movie_has_movies(self):
        set_auth_token(self.client, DIRECTOR_TOKEN)

        payload = {'actors': []}
        movie_id = None
        expected = None
        with self.app.app_context():
            mock_actors = mock_data['actors_b']
            expected_actors = []
            actors = []
            for mock_actor in mock_actors:
                actor = Actor(**mock_actor)
                actor.insert()

                actors.append(actor)
                payload['actors'].append(actor.id)
                expected_actors.append({
                    'id': actor.id,
                    **mock_actor
                })

            payload['actors'].pop()
            expected_actors.pop()

            mock_movie = mock_data['movie_a']
            movie = Movie(**mock_movie)
            movie.actors = actors
            movie.insert()
            movie_id = movie.id

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

        response = self.client.patch(f'/movies/{movie_id}', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = response.get_json()
        self.assertEqual(data, expected)

    def test_update_movie_when_unkown_argument_provided(self):
        set_auth_token(self.client, DIRECTOR_TOKEN)

        payload = None
        movie_id = None
        expected = None
        with self.app.app_context():
            mock_movie = mock_data['movie_a']
            movie = Movie(**mock_movie)
            movie.insert()
            movie_id = movie.id

            payload = {'genre': 'Drama'}

            expected = {
                'success': False,
                'description': 'The request parameters are not valid.',
                'invalid_params': [{
                    'name': 'genre',
                    'reason': 'Unknown field.'
                }]
            }

        response = self.client.patch(f'/movies/{movie_id}', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = response.get_json()
        self.assertEqual(data, expected)

    def test_update_movie_when_movie_not_found(self):
        set_auth_token(self.client, DIRECTOR_TOKEN)

        movie_id = 24
        payload = {}
        expected = {
            'success': False,
            'description': 'A movie with the id "24" was not found.',
        }

        response = self.client.patch(f'/movies/{movie_id}', json=payload)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = response.get_json()
        self.assertEqual(data, expected)


if __name__ == '__main__':
    main()

from flask import Blueprint, jsonify
from werkzeug.exceptions import NotFound
from marshmallow import ValidationError
from sqlalchemy.orm import load_only

from models.casting import Actor, Movie
from schema import ActorSchema, MovieSchema
from auth import requires_auth
from util import load_data


casting_blueprint = Blueprint('casting', __name__)

@casting_blueprint.route('/actors')
@requires_auth('get:actors')
def retrieve_actors(token):
    actors = Actor.query.all()
    schema = ActorSchema()
    serialized = [
        schema.dump(actor)
        for actor in actors
    ]

    return jsonify({
        'success': True,
        'data': serialized
    })


@casting_blueprint.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def create_actor(token):
    schema = ActorSchema()
    data = load_data(schema)

    movie_ids = data['movie_ids']
    movies = Movie.query.\
        filter(Movie.id.in_(movie_ids)).\
        options(load_only('id')).\
        all()

    actor = Actor(
        name=data['name'],
        age=data['age'],
        gender=data['gender'],
        movies=movies
    )
    actor.insert()
    serialized = [schema.dump(actor)]

    return jsonify({
        'success': True,
        'data': serialized
    })


@casting_blueprint.route('/actors/<actor_id>', methods=['PATCH'])
@requires_auth('patch:actors')
def update_actor(actor_id, token):
    schema = ActorSchema()
    data = load_data(schema, partial=True)

    actor = Actor.query.\
        filter(Actor.id == actor_id).\
        one_or_none()

    if not actor:
        raise NotFound(
            description=f'An actor with the id "{actor_id}" was not found.'
        )

    if 'name' in data:
        actor.name = data['name']
    if 'age' in data:
        actor.age = data['age']
    if 'gender' in data:
        actor.gender = data['gender']
    if 'movie_ids' in data:
        movie_ids = data['movie_ids']
        movies = Movie.query.\
            filter(Movie.id.in_(movie_ids)).\
            options(load_only('id')).\
            all()

        actor.movies = movies

    actor.update()
    serialized = [schema.dump(actor)]

    return jsonify({
        'success': True,
        'data': serialized
    })


@casting_blueprint.route('/actors/<actor_id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(actor_id, token):
    actor = Actor.query.\
        filter(Actor.id == actor_id).\
        one_or_none()

    if not actor:
        raise NotFound(
            description=f'An actor with the id "{actor_id}" was not found.'
        )

    actor.delete()

    return jsonify({
        'success': True,
        'id': actor.id
    })


@casting_blueprint.route('/movies')
@requires_auth('get:movies')
def retrieve_movies(token):
    movies = Movie.query.all()
    schema = MovieSchema()
    serialized = [
        schema.dump(movie)
        for movie in movies
    ]

    return jsonify({
        'success': True,
        'data': serialized
    })


@casting_blueprint.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def create_movie(token):
    schema = MovieSchema()
    data = load_data(schema, partial=True)

    actor_ids = data['actor_ids']
    actors = Actor.query.\
        filter(Actor.id.in_(actor_ids)).\
        options(load_only('id')).\
        all()

    release_date = data['release_date'].replace(tzinfo=None)
    movie = Movie(
        title=data['title'],
        release_date=release_date,
        actors=actors
    )
    movie.insert()
    serialized = [schema.dump(movie)]

    return jsonify({
        'success': True,
        'data': serialized
    })

from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest
from marshmallow import ValidationError
from sqlalchemy.orm import load_only

from models.casting import Actor, Movie
from schema import ActorSchema, MovieSchema
from auth import requires_auth


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
    if not request.data:
        raise BadRequest(
            description='The request did not contain a request body.'
        )

    if not request.is_json:
        raise BadRequest(
            description='The request expected a JSON request body.'
        )

    schema = ActorSchema()
    data = schema.load(request.get_json())

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

    return jsonify({
        'success': True,
        'id': actor.id
    })

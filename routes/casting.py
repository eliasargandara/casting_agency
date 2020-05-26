from flask import Blueprint, jsonify
from models.casting import Actor, Movie
from schema import ActorSchema, MovieSchema
from auth import requires_auth

actor_schema = ActorSchema()
movie_schema = MovieSchema()
casting_blueprint = Blueprint('casting', __name__)

@casting_blueprint.route('/actors')
@requires_auth('get:actors')
def retrieve_actors(token):
    actors = Actor.query.all()
    serialized = [
        actor_schema.dump(actor)
        for actor in actors
    ]

    return jsonify({
        'success': True,
        'data': serialized
    })

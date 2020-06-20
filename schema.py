from marshmallow import (
    Schema,
    fields,
    validate,
    validates,
    ValidationError
)
from sqlalchemy.orm import load_only
from models.casting import Actor, Movie


def create_not_found_messages(provided_ids, existing_ids, message):
    missing_ids = set(provided_ids) - set(existing_ids)
    indexes = {
        id: index
        for index, id in enumerate(provided_ids)
    }
    messages = {
        indexes[id]: [message.format(id)]
        for id in missing_ids
    }
    return messages


class ActorSchema(Schema):
    id = fields.Integer(
        dump_only=True
    )

    name = fields.String(
        required=True
    )

    age = fields.Integer(
        required=True
    )

    gender = fields.String(
        required=True,
        validate=validate.OneOf(['male', 'female', 'other'])
    )

    movies = fields.List(
        fields.Nested(
            lambda: MovieSchema(exclude=['actors'])
        ),
        missing=[],
        dump_only=True,
    )

    movie_ids = fields.List(
        fields.Integer(),
        data_key='movies',
        missing=[],
        load_only=True
    )

    @validates('movie_ids')
    def validate_movies_exist(self, provided_ids):
        if provided_ids:
            movies = Movie.query.\
                filter(Movie.id.in_(provided_ids)).\
                options(load_only('id')).\
                all()
            movie_ids = [movie.id for movie in movies]

            if len(provided_ids) != len(movie_ids):
                messages = create_not_found_messages(
                    provided_ids,
                    movie_ids,
                    self.error_messages['not_found']
                )
                raise ValidationError(messages)

    error_messages = {
        'not_found': 'A movie with the id "{}" was not found.'
    }

    class Meta:
        ordered = True


class MovieSchema(Schema):
    id = fields.Integer(
        dump_only=True
    )

    title = fields.String(
        required=True
    )

    release_date = fields.DateTime(
        required=True
    )

    actors = fields.List(
        fields.Nested(
            lambda: ActorSchema(exclude=['movies'])
        ),
        missing=[],
        dump_only=True
    )

    actor_ids = fields.List(
        fields.Integer(),
        data_key='actors',
        missing=[],
        load_only=True
    )

    @validates('actor_ids')
    def validate_actors_exist(self, provided_ids):
        if provided_ids:
            actors = Actor.query.\
                filter(Actor.id.in_(provided_ids)).\
                options(load_only('id')).\
                all()
            actor_ids = {actor.id for actor in actors}

            if len(provided_ids) != len(actor_ids):
                messages = create_not_found_messages(
                    provided_ids,
                    actor_ids,
                    self.error_messages['not_found']
                )
                raise ValidationError(messages)

    error_messages = {
        'not_found': 'An actor with the id "{}" was not found.'
    }

    class Meta:
        ordered = True

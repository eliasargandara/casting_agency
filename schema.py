from marshmallow import Schema, fields

class ActorSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    age = fields.Int()
    gender = fields.Str()


class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    release_date = fields.DateTime()

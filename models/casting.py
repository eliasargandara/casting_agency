from sqlalchemy import Column, String, Integer, TIMESTAMP
from models.database import db


actor_movie_relation = db.Table(
    'actor_movie',
    db.Column(
        'actor_id',
        db.Integer,
        db.ForeignKey('actor.id', ondelete='CASCADE'),
        primary_key=True
    ),
    db.Column(
        'movie_id',
        db.Integer,
        db.ForeignKey('movie.id', ondelete='CASCADE'),
        primary_key=True
    )
)

class Actor(db.Model):
    __tablename__ = 'actor'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)

    movies = db.relationship(
        'Movie',
        secondary=actor_movie_relation,
        backref='actors',
        passive_deletes=True
    )

    def __repr__(self):
        return f'<Actor id: {self.id}, name: {self.name}>'

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class Movie(db.Model):
    __tablename__ = 'movie'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(TIMESTAMP, nullable=False)

    def __repr__(self):
        return f'<Movie id: {self.id}, title: {self.title}>'

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

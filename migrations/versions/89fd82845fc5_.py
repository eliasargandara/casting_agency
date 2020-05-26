"""empty message

Revision ID: 89fd82845fc5
Revises: 
Create Date: 2020-05-25 15:38:39.247296

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89fd82845fc5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'actor',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('age', sa.Integer(), nullable=False),
        sa.Column('gender', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'movie',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('release_date', sa.TIMESTAMP(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'actor_movie',
        sa.Column('actor_id', sa.Integer(), nullable=False),
        sa.Column('movie_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['actor_id'], ['actor.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(
            ['movie_id'], ['movie.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('actor_id', 'movie_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('actor_movie')
    op.drop_table('movie')
    op.drop_table('actor')
    # ### end Alembic commands ###

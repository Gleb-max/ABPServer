import sqlalchemy as sa
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


from sqlalchemy import orm
from data.db_session import db


class StudyDirection(db.Model, SerializerMixin):
    __tablename__ = "study_direction"
    serialize_rules = ( '-enrolls', )

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, unique=True)

    # Relationships
    enrolls = orm.relationship("Enrollee", back_populates="study_direction")

    name = sa.Column(sa.String(100), nullable=False)
    # budget_count = sa.Column(sa.SmallInteger(), nullable=True)
    description = sa.Column(sa.Text, nullable=True)


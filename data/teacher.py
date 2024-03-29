import sqlalchemy as sa
from sqlalchemy_serializer import SerializerMixin

from sqlalchemy import orm
from data.db_session import db


class Teacher(db.Model, SerializerMixin):
    __tablename__ = "teacher"
    serialize_rules = ('-directions', '-subjects')

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, unique=True)

    full_name = sa.Column(sa.String(200), nullable=True)
    rank = sa.Column(sa.String(50), nullable=True)
    post = sa.Column(sa.String(50), nullable=True)
    email = sa.Column(sa.String(50), nullable=True)
    photo = sa.Column(sa.String(200), nullable=True)

    # relationships
    subjects = orm.relationship("Subject", back_populates="teacher")

    def __init__(self, full_name, rank=None, post=None, email=None, photo=None, subjects=[]):
        self.full_name = full_name
        self.rank = rank
        self.post = post
        self.photo = photo
        self.email = email
        self.subjects = subjects


    def __str__(self):
        if self.full_name:
            return self.full_name

        return "teacher"
import sqlalchemy as sa
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from sqlalchemy import orm
from data.db_session import db
from data.enrollee import Enrollee


class IndividualAchievement(db.Model, SerializerMixin):
    __tablename__ = "individual_achievement"
    serialize_rules = ( '-enrolls', )

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, unique=True)

    enrolls = orm.relationship("Enrollee", secondary=Enrollee.association_table,
                               back_populates='individual_achievement_list')

    name = sa.Column(sa.String(100), nullable=False)
    additional_score = sa.Column(sa.SmallInteger, nullable=False)

    def __init__(self):
        self.additional_score = 10

    def __str__(self):
        return self.name
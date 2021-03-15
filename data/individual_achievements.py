import sqlalchemy as sa
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


from sqlalchemy import orm
from data.db_session import db


class IndividualAchievement(db.Model):
    __tablename__ = "individual_achievement"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, unique=True)

    # Relationships
    enrollee = orm.relationship("Enrollee", back_populates="individual_achievement_list", uselist=False)

    name = sa.Column(sa.String(100), nullable=False)
    additional_score = sa.Column(sa.SmallInteger, nullable=False)


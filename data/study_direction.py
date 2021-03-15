import sqlalchemy as sa
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


from sqlalchemy import orm
from data.db_session import db


class StudyDirection(db.Model):
    __tablename__ = "study_direction"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    # Relationships
    enrollee_id = sa.Column(sa.Integer, sa.ForeignKey('enrollee.id'))
    enrollee = orm.relationship("Enrollee", back_populates="study_direction")

    name = sa.Column(sa.String(100), nullable=False)
    description = sa.Column(sa.Text, nullable=True)


import sqlalchemy as sa
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class StudyDirection(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = "study_direction"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    # Relationships
    enrollee_id = sa.Column(sa.Integer, sa.ForeignKey('enrollee.id'))
    enrollee = orm.relationship("Enrollee", back_populates="study_direction")

    name = sa.Column(sa.String(100), nullable=False)
    description = sa.Column(sa.Text, nullable=True)


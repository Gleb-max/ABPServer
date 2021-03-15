import sqlalchemy as sa
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from data.db_session import db


class Passport(db.Model):
    __tablename__ = "passport"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    # Relationships
    enrollee_id = sa.Column(sa.Integer, sa.ForeignKey('enrollee.id'))
    enrollee = orm.relationship("Enrollee", back_populates="passport")


    series = sa.Column(sa.String(length=10), nullable=True)
    number = sa.Column(sa.String(length=10), nullable=True)
    who_issued = sa.Column(sa.String(length=200), nullable=True)
    department_code = sa.Column(sa.Integer(), nullable=True)
    when_issued = sa.Column(sa.Date, nullable=True)
    passport_scan = sa.Column(sa.String(300), nullable=True)
    registration_address = sa.Column(sa.Text, nullable=True)


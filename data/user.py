import sqlalchemy as sa
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    name = sa.Column(sa.String(length=100))
    surname = sa.Column(sa.String(length=100))
    last_name = sa.Column(sa.String(length=100))

    is_male = sa.Column(sa.Boolean(), nullable=True, default=None)
    email = sa.Column(sa.String(length=100), nullable=False)
    password = sa.Column(sa.String(length=30), nullable=False)

    account_type = sa.Column(sa.SmallInteger(), nullable=False, default=0)
    # 0 - абитурент
    enrollee = orm.relationship('Enrollee', uselist=False, back_populates="user")

    def __init__(self, name, surname, last_name, is_male, email, password, account_type=0):
        self.name = name
        self.surname = surname
        self.last_name = last_name
        self.is_male = is_male
        self.email = email
        self.password = password
        self.account_type = account_type

    def __str__(self):
        return f"<{self.name} {self.surname} {self.last_name}>"

    def __repr__(self):
        return self.__str__()

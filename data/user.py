import sqlalchemy as sa
from sqlalchemy_serializer import SerializerMixin

from data import student
from sqlalchemy import orm
from data.db_session import db
from data.enrollee import Enrollee


class User(db.Model, SerializerMixin):
    __tablename__ = "users"
    serialize_rules = ('-enrollee', )

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, unique=True)
    login = sa.Column(sa.String(length=100), nullable=True)

    name = sa.Column(sa.String(length=100))
    surname = sa.Column(sa.String(length=100))
    last_name = sa.Column(sa.String(length=100))

    is_male = sa.Column(sa.Boolean(), nullable=True, default=None)
    email = sa.Column(sa.String(length=100), nullable=False)
    password = sa.Column(sa.String(length=30), nullable=False)

    account_type = sa.Column(sa.SmallInteger(), nullable=False, default=0)
    # 0 - абитурент
    enrollee = orm.relationship('Enrollee', uselist=False, back_populates="user")
    # 1 - студент
    student = orm.relationship('Student', uselist=False, back_populates="user")

    def __init__(self, name, surname, last_name, is_male, email, password, account_type=0):
        self.name = name
        self.surname = surname
        self.last_name = last_name
        self.is_male = is_male
        self.email = email
        self.password = password
        self.account_type = account_type
        self.enrollee = Enrollee()
        db.session.add(self.enrollee)
        db.session.commit()

    def __str__(self):
        return f"<{self.name} {self.surname} {self.last_name}>"

    def __repr__(self):
        return self.__str__()

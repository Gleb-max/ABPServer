import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class User(SqlAlchemyBase, UserMixin, SerializerMixin):

    __tablename__ = "users"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    phone = sqlalchemy.Column(sqlalchemy.types.String, nullable=False, index=True, unique=True)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    tg_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    receipts = orm.relation("Receipt", back_populates="user")

    def __str__(self):
        return f"<User phone = {self.phone}>"

    def __repr__(self):
        return self.__str__()

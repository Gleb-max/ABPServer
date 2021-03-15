import sqlalchemy

from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from data.db_session import db


class Receipt(db.Model):

    __tablename__ = "receipts"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    scan_code = sqlalchemy.Column(sqlalchemy.String,
                                  index=True, unique=False, nullable=False)
    receipt = sqlalchemy.Column(sqlalchemy.Binary, nullable=False)
    date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relation("User")

    def __str__(self):
        return f"<Receipt scan_code = {self.scan_code}>"

    def __repr__(self):
        return self.__str__()

import sqlalchemy as sa
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class ExamInfo(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = "exam_info"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    # Relationships
    _enrollee = orm.relationship("Enrollee", back_populates="exam_data_list", uselist=False)

    name = sa.Column(sa.String(100), nullable=False)
    grade = sa.Column(sa.SmallInteger, nullable=False)


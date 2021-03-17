import sqlalchemy as sa
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


from sqlalchemy import orm
from data.db_session import db


class ExamInfo(db.Model, SerializerMixin):
    __tablename__ = "exam_info"
    serialize_rules = ( '-enrollee', )

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, unique=True)

    # Relationships
    enrollee_id = sa.Column(sa.Integer, sa.ForeignKey('enrollee.id', ondelete='CASCADE'))
    enrollee = orm.relationship("Enrollee", back_populates="exam_data_list", uselist=True)

    name = sa.Column(sa.String(100), nullable=False)
    grade = sa.Column(sa.SmallInteger, nullable=False)

    def __init__(self, name, grade):
        self.name = name
        self.grade = grade


    def __str__(self):
        if self.name and self.grade:
            return f'{self.name} = {self.grade}'
        else:
            return 'Exam info'



import sqlalchemy as sa
from sqlalchemy_serializer import SerializerMixin

from sqlalchemy import orm
from data.db_session import db


class Subject(db.Model, SerializerMixin):
    __tablename__ = "subject"
    serialize_rules = ('-students_group') # TODO

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, unique=True)

    name = sa.Column(sa.String(100), nullable=True)
    cabinet_number = sa.Column(sa.Integer, nullable=True)

    # relationships
    students_group_id = sa.Column(sa.Integer, sa.ForeignKey('students_group.id'))
    students_group = orm.relationship("StudentsGroup", back_populates="subjects")

    teacher_id = sa.Column(sa.Integer, sa.ForeignKey('teacher.id'))
    from data.teacher import Teacher
    teacher = orm.relationship(Teacher, back_populates="subjects")

    def __str__(self):
        if self.name:
            return self.name

        return "subject"
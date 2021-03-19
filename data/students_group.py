import sqlalchemy as sa
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin

from sqlalchemy import orm, select, func
from data.db_session import db
from data.study_direction import StudyDirection


class StudentsGroup(db.Model, SerializerMixin):
    __tablename__ = "students_group"
    serialize_rules = ('-user', '-students')  # TODO

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, unique=True)

    # Common information
    name = sa.Column(sa.String(50), nullable=True)

    # Relationships
    direction_id = sa.Column(sa.Integer, sa.ForeignKey('study_direction.id'))
    direction = orm.relationship(StudyDirection, back_populates="groups")

    students = orm.relationship("Student", back_populates="student_group")
    subjects = orm.relationship("Subject", back_populates="students_group")

    def __init__(self, name):
        self.name = name

    def __str__(self):
        if self.name:
            return f'Группа {self.name}'

        return f"<StudentsGroup>"

    def __repr__(self):
        return self.__str__()

import sqlalchemy as sa
from sqlalchemy_serializer import SerializerMixin

from sqlalchemy import orm
from data.db_session import db


class Subject(db.Model, SerializerMixin):
    __tablename__ = "subject"
    serialize_rules = ('-students_group', '-students_group') # TODO

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, unique=True)

    name = sa.Column(sa.String(100), nullable=True)
    cabinet_number = sa.Column(sa.Integer, nullable=True)

    sub_association_table = sa.Table('sub_group_association', db.metadata,
                                     sa.Column('subject_id', sa.Integer, sa.ForeignKey('subject.id')),
                                     sa.Column('students_group_id', sa.Integer, sa.ForeignKey('students_group.id'))
                              )

    # relationships
    # students_group_id = sa.Column(sa.Integer, sa.ForeignKey('students_group.id'))
    students_group = orm.relationship("StudentsGroup", back_populates="subjects",
                                      secondary=sub_association_table)

    # teacher_id = sa.Column(sa.Integer, sa.ForeignKey('teacher.id'))
    # from data.teacher import Teacher
    # teacher = orm.relationship(Teacher, back_populates="subjects")
    # teacher_pk = sa.Column(sa.Integer, nullable=True)

    def __init__(self, name):
        self.name = name


    def __str__(self):
        if self.name:
            return self.name

        return "subject"
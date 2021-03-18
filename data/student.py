from datetime import datetime, timedelta

import sqlalchemy as sa
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin

from sqlalchemy import orm, select, func
from data.db_session import db
from data.students_group import StudentsGroup
from data import enrollee_statuses
from data.study_direction import StudyDirection


class Student(db.Model, SerializerMixin):
    __tablename__ = "student"
    serialize_rules = ('-user',)

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, unique=True)

    # Relationships
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), nullable=True)
    user = orm.relationship("User", back_populates="student")

    student_group_id = sa.Column(sa.Integer, sa.ForeignKey('students_group.id'))
    student_group = orm.relationship(StudentsGroup, back_populates="students")


    # Common information
    card_number = sa.Column(sa.Integer(), nullable=True)
    record_book_number = sa.Column(sa.Integer(), nullable=True)
    library_card_number = sa.Column(sa.Integer(), nullable=True)
    enrollment_date = sa.Column(sa.Date(), nullable=True)
    expiration_date = sa.Column(sa.Date(), nullable=True)

    def __init__(self):
        base_number = 100
        library_base_number = 1000

        try:
            base_number_record_book_number = 1000
            self.record_book_number = base_number_record_book_number + Student.query.count() + 1
        except Exception as e:
            print(e)

        self.card_number = base_number + Student.query.count() + 1
        self.library_card_number = library_base_number + Student.query.count() + 1
        self.enrollment_date = datetime.now().date()
        self.expiration_date = datetime.now().date() + timedelta(days=365 * 4)

    def __str__(self):
        if self.user:
            if self.user.name and self.user.surname:
                return f'{self.user.name} {self.user.surname}'

        return f"Student"

    def __repr__(self):
        return self.__str__()

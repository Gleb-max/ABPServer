from datetime import datetime, timedelta

import sqlalchemy as sa
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin

from sqlalchemy import orm, select, func
from data.db_session import db
from data import enrollee_statuses
from data.study_direction import StudyDirection


class Student(db.Model, SerializerMixin):
    __tablename__ = "student"
    serialize_rules = ('-user',)
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, unique=True)

    # Relationships
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), nullable=False)
    user = orm.relationship("User", back_populates="student")

    # Common information
    group_number = sa.Column(sa.String(20), nullable=True)
    card_number = sa.Column(sa.Integer, nullable=True)
    record_book_number = sa.Column(sa.Integer, nullable=True)
    library_card_number = sa.Column(sa.Integer, nullable=True)
    enrollment_date = sa.Column(sa.Date, nullable=True)
    expiration_date = sa.Column(sa.Date, nullable=True)

    # def __init__(self, group_number=None, user=None):
    #     base_number = 100
    #     library_base_number = 1000
    #     self.card_number = base_number + Student.query.count() + 1
    #     self.library_card_number = library_base_number + Student.query.count() + 1
    #
    #     if user and user.enrollee and user.enrollee.study_direction_id:
    #         self.record_book_number = StudyDirection.query.filter_by(id=user.enrollee.study_direction_id).count() + 1
    #         # self.user_id = user.id
    #         # self.user = user
    #
    #     self.enrollment_date = datetime.now().date()
    #     self.expiration_date = datetime.now().date() + timedelta(days=365 * 4)
    #     self.group_number = group_number

    def __str__(self):
        if self.user:
            if self.user.name and self.user.surname:
                return f'{self.user.name} {self.user.surname}'

        return f"<Enrollee>"

    def __repr__(self):
        return self.__str__()

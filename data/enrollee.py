import sqlalchemy as sa
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Enrollee(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = "enrollee"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    # Relationships
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    user = orm.relationship("User", back_populates="enrollee")
    passport = orm.relationship("Passport", uselist=False, back_populates="enrollee")
    school_certificate = orm.relationship("SchoolCertificate", uselist=False, back_populates="enrollee")
    study_direction = orm.relationship("StudyDirection", uselist=False, back_populates="enrollee")
    # Individual achievement
    individual_achievement_id = sa.Column(sa.Integer, sa.ForeignKey('individual_achievement.id'))
    individual_achievement_list = orm.relationship("IndividualAchievement", back_populates="enrollee")
    # Exam data
    exam_data_id = sa.Column(sa.Integer, sa.ForeignKey('exam_info.id'))
    exam_data_list = orm.relationship("ExamInfo", back_populates="_enrollee")

    # Common information
    birthday = sa.Column(sa.Date, nullable=False)
    phone = sa.Column(sa.String(20), nullable=True)
    birth_place = sa.Column(sa.String(200), nullable=False)
    need_hostel = sa.Column(sa.Boolean, nullable=True)
    photo = sa.Column(sa.String(length=300), nullable=True)
    agreement_scan = sa.Column(sa.String(300), nullable=True)
    is_budgetary = sa.Column(sa.Boolean)
    original_or_copy = sa.Column(sa.Boolean, nullable=True)
    enrollment_consent = sa.Column(sa.String(length=500), nullable=True)

    def __str__(self):
        return f"<{self.name} {self.surname} {self.last_name}>"

    def __repr__(self):
        return self.__str__()

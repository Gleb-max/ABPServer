import sqlalchemy as sa
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from sqlalchemy import orm, MetaData
from data.db_session import db
from data.db_session import association_table


class Enrollee(db.Model):
    __tablename__ = "enrollee"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, unique=True)

    # Relationships
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    user = orm.relationship("User", back_populates="enrollee")
    passport = orm.relationship("Passport", uselist=False, back_populates="enrollee")
    school_certificate = orm.relationship("SchoolCertificate", uselist=False, back_populates="enrollee")
    study_direction = orm.relationship("StudyDirection", uselist=True, back_populates="enrollee")

    # Individual achievement
    # individual_achievement_id = sa.Column(sa.Integer, sa.ForeignKey('individual_achievement.id'))
    # individual_achievement_list = orm.relationship("IndividualAchievement", back_populates="enrollee")
    # individual_achievement_list = orm.relationship("IndividualAchievement",
    #                                                secondary=association_table,
    #                                                back_populates='enrolls')

    # Exam data
    exam_data_id = sa.Column(sa.Integer, sa.ForeignKey('exam_info.id'))
    exam_data_list = orm.relationship("ExamInfo", back_populates="_enrollee")

    # Common information
    birthday = sa.Column(sa.Date, nullable=True)
    phone = sa.Column(sa.String(20), nullable=True)
    birth_place = sa.Column(sa.String(200), nullable=True)
    need_hostel = sa.Column(sa.Boolean, nullable=True)
    photo = sa.Column(sa.BLOB, nullable=True)
    agreement_scan = sa.Column(sa.BLOB, nullable=True)
    is_budgetary = sa.Column(sa.Boolean)
    original_or_copy = sa.Column(sa.Boolean, nullable=True)
    enrollment_consent = sa.Column(sa.BLOB, nullable=True)

    def __init__(self, birthday=None, phone=None, birth_place=None, need_hostel=None, photo=None, agreement_scan=None,
                 is_budgetary=None, original_or_copy=None, enrollment_consent=None):
        self.birthday = birthday
        self.phone = phone
        self.birth_place = birth_place
        self.need_hostel = need_hostel
        self.photo = photo
        self.agreement_scan = agreement_scan
        self.is_budgetary = is_budgetary
        self.original_or_copy = original_or_copy
        self.enrollment_consent = enrollment_consent
        # TODO photo uploading

    def __str__(self):
        return f"<{self.user.name}>"

    def __repr__(self):
        return self.__str__()

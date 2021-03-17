import sqlalchemy as sa
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin

from sqlalchemy import orm, select, func
from data.db_session import db
from data import enrollee_statuses
from data.passport import Passport
from data.school_certificate import SchoolCertificate
from data.exam_info import ExamInfo
from sqlalchemy import case


class Enrollee(db.Model, SerializerMixin):
    __tablename__ = "enrollee"
    serialize_rules = ('-user',)
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, unique=True)

    # Exam data
    exam_data_list = orm.relationship(ExamInfo, back_populates="enrollee", uselist=True, cascade="all,delete")

    # Common information
    birthday = sa.Column(sa.Date, nullable=True)
    phone = sa.Column(sa.String(20), nullable=True)
    birth_place = sa.Column(sa.String(200), nullable=True)
    need_hostel = sa.Column(sa.Boolean, nullable=True)
    photo = sa.Column(sa.String(500), nullable=True)
    agreement_scan = sa.Column(sa.String(500), nullable=True)
    is_budgetary = sa.Column(sa.Boolean)
    original_or_copy = sa.Column(sa.Boolean, nullable=True)
    enrollment_consent = sa.Column(sa.String(500), nullable=True)
    status = sa.Column(sa.Integer, nullable=True, default=enrollee_statuses.NEW)
    consideration_stage = sa.Column(sa.Integer, nullable=True, default=enrollee_statuses.NEW)

    # Relationships
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'))
    user = orm.relationship("User", back_populates="enrollee")

    passport = orm.relationship(Passport, uselist=False, back_populates="enrollee", cascade="all,delete")
    school_certificate = orm.relationship(SchoolCertificate, uselist=False, back_populates="enrollee",
                                          cascade="all,delete")

    study_direction_id = sa.Column(sa.Integer, sa.ForeignKey('study_direction.id', ondelete='CASCADE'))
    study_direction = orm.relationship("StudyDirection", back_populates='enrolls')

    association_table = sa.Table('association', db.metadata,
                                 sa.Column('enrollee_id', sa.Integer, sa.ForeignKey('enrollee.id', ondelete='CASCADE')),
                                 sa.Column('individual_achievement_id', sa.Integer,
                                           sa.ForeignKey('individual_achievement.id', ondelete='CASCADE'))
                                 )
    individual_achievement_list = orm.relationship("IndividualAchievement",
                                                   secondary=association_table,
                                                   back_populates='enrolls', cascade="all,delete")

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

    def __str__(self):
        if self.user:
            if self.user.name and self.user.surname:
                return f'{self.user.name} {self.user.surname}'

        return f"<Enrollee>"

    def __repr__(self):
        return self.__str__()

    def get_individual_grade(self):
        total = 0
        for achievement in self.individual_achievement_list:
            total += achievement.additional_score
        return min(10, total)

    def get_exam_total_grade(self):
        total = 0
        for subject in self.exam_data_list:
            total += subject.grade
        return total

    @hybrid_property
    def get_total_grade(self):
        return self.get_exam_total_grade() + self.get_individual_grade()

    @get_total_grade.expression
    def get_total_grade_exp(cls):
        return (select([func.count(Enrollee.id)])
                .where(Enrollee.id == cls.id))



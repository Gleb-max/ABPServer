import sqlalchemy as sa

from sqlalchemy import orm
from data.db_session import db


class SchoolCertificate(db.Model):
    __tablename__ = "school_certificate"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, unique=True)

    # Relationships
    enrollee_id = sa.Column(sa.Integer, sa.ForeignKey('enrollee.id'))
    enrollee = orm.relationship("Enrollee", back_populates="school_certificate")

    certificate_number = sa.Column(sa.Integer, nullable=True)
    certificate_scan = sa.Column(sa.String(300), nullable=True)

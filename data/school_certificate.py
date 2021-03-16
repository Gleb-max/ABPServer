import sqlalchemy as sa

from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from data.db_session import db


class SchoolCertificate(db.Model, SerializerMixin):
    __tablename__ = "school_certificate"
    serialize_rules = ( '-enrollee', )

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, unique=True)

    # Relationships
    enrollee_id = sa.Column(sa.Integer, sa.ForeignKey('enrollee.id', ondelete='CASCADE'))
    enrollee = orm.relationship("Enrollee", back_populates="school_certificate")

    certificate_number = sa.Column(sa.Integer, nullable=True)
    certificate_scan = sa.Column(sa.String(300), nullable=True)

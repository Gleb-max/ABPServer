import sqlalchemy as sa
from sqlalchemy_serializer import SerializerMixin


from sqlalchemy import orm
from data.db_session import db
from data.faculty import Faculty


class StudyDirection(db.Model, SerializerMixin):
    __tablename__ = "study_direction"
    serialize_rules = ( '-enrolls', '-groups')

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, unique=True)

    # Relationships
    enrolls = orm.relationship("Enrollee", back_populates="study_direction")

    faculty = orm.relationship(Faculty, back_populates='directions')
    faculty_id = sa.Column(sa.Integer, sa.ForeignKey('faculty.id', ondelete='CASCADE'))

    groups = orm.relationship("StudentsGroup", back_populates="direction")


    name = sa.Column(sa.String(100), nullable=False)
    budget_count = sa.Column(sa.SmallInteger(), nullable=True)
    description = sa.Column(sa.Text, nullable=True)


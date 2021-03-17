import sqlalchemy as sa
from sqlalchemy_serializer import SerializerMixin


from sqlalchemy import orm
from data.db_session import db


class Faculty(db.Model, SerializerMixin):
    __tablename__ = "faculty"
    serialize_rules = ('-directions', '-dean')

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, unique=True)

    # Relationships
    directions = orm.relationship("StudyDirection", back_populates="faculty")

    name = sa.Column(sa.String(100), nullable=False)
    description = sa.Column(sa.Text, nullable=True)

    def __str__(self):
        if self.name:
            return self.name

        return "faculty no name"
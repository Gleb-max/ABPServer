import sqlalchemy as sa
from sqlalchemy_serializer import SerializerMixin

from sqlalchemy import orm
from data.db_session import db


class Dean(db.Model, SerializerMixin):
    __tablename__ = "dean"
    serialize_rules = ('-user',)

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, unique=True)

    # Relationships
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), nullable=True)
    user = orm.relationship("User", back_populates="dean")
    faculty = orm.relationship('Faculty', uselist=False, back_populates="dean")

    # generic information

    post = sa.Column(sa.String(length=90), nullable=True)
    phone = sa.Column(sa.String(length=20), nullable=True)

    def __str__(self):
        if self.user:
            if self.user.name and self.faculty and self.faculty.name:
                return f'{self.user.name} {self.post} - {self.faculty.name}'

        return f"Dean"

    def __repr__(self):
        return self.__str__()

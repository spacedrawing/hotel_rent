import datetime
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'user'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String)
    patronymic = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    age = sqlalchemy.Column(sqlalchemy.Integer)
    # address = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='SPB')
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='')
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True, default='')
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    creation_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    reviews = orm.relationship("Review", back_populates="user")

    def __repr__(self):
        return f"<User> {self.id} {self.surname} {self.name}"

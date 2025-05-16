import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Hotel(SqlAlchemyBase):
    __tablename__ = 'hotel'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    image = sqlalchemy.Column(sqlalchemy.String)
    alternative = sqlalchemy.Column(sqlalchemy.String)
    title = sqlalchemy.Column(sqlalchemy.String)
    city = sqlalchemy.Column(sqlalchemy.String)
    price = sqlalchemy.Column(sqlalchemy.String)
    rating = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
    conveniences = sqlalchemy.Column(sqlalchemy.String)
    reviews = orm.relationship("Review", back_populates="hotel")
    rooms = orm.relationship("Room", back_populates="hotel")

import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Room(SqlAlchemyBase):
    __tablename__ = 'rooms'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    hotel_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('hotel.id'))
    hotel = orm.relationship('Hotel', back_populates='rooms')

    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.String)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    capacity = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

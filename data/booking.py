import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Booking(SqlAlchemyBase):
    __tablename__ = 'bookings'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    room_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("rooms.id"))
    room = orm.relationship("Room")

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))
    user = orm.relationship("User")

    start_date = sqlalchemy.Column(sqlalchemy.Date, nullable=False)
    end_date = sqlalchemy.Column(sqlalchemy.Date, nullable=False)

import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

class Review(SqlAlchemyBase):
    __tablename__ = 'review'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='')
    rating = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))
    user = orm.relationship("User", back_populates='reviews')
    hotel_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("hotel.id"))
    hotel = orm.relationship("Hotel", back_populates='reviews')
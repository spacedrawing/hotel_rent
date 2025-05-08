import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Hotel(SqlAlchemyBase):
    __tablename__ = 'hotel'

    
from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class EmptyTime(Base):
    __tablename__ = 'empty_time'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    weekday = Column(String, nullable=False)  # e.g., 'Monday'
    # List of periods e.g., ['08:00-10:00', '14:00-16:00']
    periods = Column(JSON, nullable=False)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, nullable=False, unique=True)
    user_pw = Column(String, nullable=False)
    user_name = Column(String, nullable=False)
    major = Column(String, nullable=False)
    empty_times = relationship('EmptyTime', backref='user')
    subjects = Column(JSON)

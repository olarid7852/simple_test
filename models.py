from sqlalchemy import Column, ForeignKey, Integer, String

from db import Base


class Team(Base):
    __tablename__ = 'team'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Member(Base):
    __tablename__ = 'member'

    id = Column(Integer, primary_key=True, nullable=True, auto_increament=True)
    team_id = Column(Integer, ForeignKey(Team.id), primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)

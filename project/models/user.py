from sqlalchemy import Column, Integer, String
from project.databases import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(160))

from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column, DateTime, ForeignKey, Numeric
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.orm import mapper
Base = declarative_base()
engine = create_engine('postgresql+psycopg2://postgres:1@localhost/forbot', echo=True)
print(engine)

metadata = MetaData('postgresql+psycopg2://postgres:1@localhost/forbot')

# class Users(Base):
#     __tablename__ = 'users'
#     user_id = Column(Integer, primary_key=True, nullable=False)

class Customer(Base):
    __table__ = Table('user_id', metadata, autoload=True)

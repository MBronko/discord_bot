from sqlalchemy import create_engine, Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Rules(Base):
    __tablename__ = 'rules'

    id = Column('id', Integer, primary_key=True)
    server = Column('server', Integer, default='')
    channel = Column('channel', Integer, default='')
    user = Column('user', Integer, default='')
    type = Column('type', String)
    value = Column('value', String, default='')
    timestamp = Column('timestamp', TIMESTAMP, server_default=func.now())


class Leaguechamps(Base):
    __tablename__ = 'leaguechamps'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String, default='')
    parsedname = Column('parsedname', String, default='')
    top = Column('top', Boolean, default=False)
    jungle = Column('jungle', Boolean, default=False)
    mid = Column('mid', Boolean, default=False)
    adc = Column('adc', Boolean, default=False)
    support = Column('support', Boolean, default=False)


class LeaguechampsKeyCache(Base):
    __tablename__ = 'LeagueChampsKeyCache'

    id = Column('id', Integer, primary_key=True)
    key = Column('key', String, default='')
    parsedname = Column('parsedname', String, default='')


class Todolist(Base):
    __tablename__ = 'todolist'

    id = Column('id', Integer, primary_key=True)
    todo_id = Column('todo_id', String)
    server_id = Column('server_id', Integer)
    msg_id = Column('msg_id', Integer, default=0)
    title = Column('title', String)
    color = Column('color', Integer)


class TodoSect(Base):
    __tablename__ = 'todosect'

    id = Column('id', Integer, primary_key=True)
    todo_id = Column('todo_id', String)
    server_id = Column('server_id', Integer)
    title = Column('title', String, default='title')
    content = Column('content', String, default='')
    done = Column('done', Boolean, default=False)
    timestamp = Column('timestamp', TIMESTAMP, server_default=func.now())


engine = create_engine('sqlite:///dcbot.db')
Base.metadata.create_all(engine)
Session = sessionmaker(engine)

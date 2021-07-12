from sqlalchemy import create_engine, Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# basically just settings for each server
class Rules(Base):
    __tablename__ = "rules"

    id = Column("id", Integer, primary_key=True)
    server = Column("server", Integer, default="")
    channel = Column("channel", Integer, default="")
    user = Column("user", Integer, default="")
    type = Column("type", String)
    value = Column("value", String, default="")
    timestamp = Column("timestamp", TIMESTAMP, server_default=func.now())


# store league of legends champions info
class Leaguechamps(Base):
    __tablename__ = "leaguechamps"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String, default="")
    top = Column("top", Boolean, default=False)
    jungle = Column("jungle", Boolean, default=False)
    mid = Column("mid", Boolean, default=False)
    adc = Column("adc", Boolean, default=False)
    support = Column("support", Boolean, default=False)


engine = create_engine('sqlite:///dcbot.db')
Base.metadata.create_all(engine)
Session = sessionmaker(engine)
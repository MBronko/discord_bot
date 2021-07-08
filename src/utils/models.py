from sqlalchemy import create_engine, Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Settings(Base):
    __tablename__ = "settings"

    id = Column("id", Integer, primary_key=True)
    server = Column("server", Integer, default="")
    channel = Column("channel", Integer, default="")
    user = Column("user", Integer, default="")
    type = Column("type", String)
    value = Column("value", String, default="")
    timestamp = Column("timestamp", TIMESTAMP, server_default=func.now())


class Leaguechamps(Base):
    __tablename__ = "leaguechamps"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String, default="")
    top = Column("top", Boolean, default=False)
    jungle = Column("jungle", Boolean, default=False)
    mid = Column("mid", Boolean, default=False)
    adc = Column("adc", Boolean, default=False)
    support = Column("support", Boolean, default=False)


# class Logs(Base):
#     __tablename__ = "logs"
#
#     id = Column("id", Integer, primary_key=True)
#     server = Column("server", Integer)
#     channel = Column("channel", Integer)
#     user = Column("user", Integer)
#     command = Column("command", String)
#     timestamp = Column("timestamp", TIMESTAMP, server_default=func.now())

print("test")
test = "asd"
engine = create_engine('sqlite:///../dcbot.db')
Base.metadata.create_all(engine)
Session = sessionmaker(engine)
# name = ["test7", "test", "broken"]

# with Session() as session:
#     new_champ = Leaguechamps()
#     new_champ.top = True
#     new_champ.name = name
#     new_champ.support = True
#
#     session.add(new_champ)
#     session.commit()

# with Session() as session:
    # for champ in session.query(Leaguechamps).filter(Leaguechamps.name.not_in(name)):
    #     print(f"{champ.name}")



        # print(f"{champ.id} {champ.name} {champ.top} {champ.jungle} {champ.mid} {champ.adc} {champ.support}")

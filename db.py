from sqlalchemy import create_engine, Column, Integer, String, text, DateTime, Boolean, Float, event
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


def create_tables(Base=Base):
    engine_streets = create_engine('sqlite:///C:\\Users\\Admin\\Desktop\\bot_real_estate\\datasets\\merged_streets.db')
    engine = create_engine("sqlite:///C:\\Users\\Admin\\Desktop\\bot_real_estate\\datasets\\users.db")
    Session = sessionmaker(bind=engine)
    Session_streets = sessionmaker(bind=engine_streets)
    Base.metadata.create_all(engine)
    Base.metadata.create_all(engine_streets)
    return Session, Session_streets

class User(Base):
    __tablename__ = 'users'
    uid = Column(Integer, primary_key=True)
    nick1 = Column(String)
    nick2 = Column(String)
    start_time = Column(DateTime) 
    messages = Column(Integer)
    active = Column(Boolean)

    def __init__(self, uid, nick1, nick2, start_time):
        self.uid = uid
        self.start_time = start_time
        self.nick1 = nick1
        self.nick2 = nick2
        self.messages = 0
        self.active = True 


class StreetName(Base):
    __tablename__ = 'street_names'
    id = Column(Integer, primary_key=True)
    street_name = Column(String, unique=True)


class CacUserData(Base):
    __tablename__ = "cac_userdata"
    user_id = Column(Integer, primary_key=True)
    chosen_region_name = Column(String)
    chosen_street_name = Column(String)
    house_info1 = Column(String)
    house_info2 = Column(String)
    number_of_rooms = Column(Integer)
    cac_age = Column(Integer)
    area = Column(Float)
    price_of_finishing = Column(String)
    repair_coef = Column(Float)
    furniture_cost = Column(Integer)


class User(Base):
    __tablename__ = 'users'
    uid = Column(Integer, primary_key=True)
    nick1 = Column(String)
    nick2 = Column(String)
    start_time = Column(DateTime) 
    messages = Column(Integer)
    active = Column(Boolean)


    def __init__(self, uid, nick1, nick2, start_time):
        self.uid = uid
        self.start_time = start_time
        self.nick1 = nick1
        self.nick2 = nick2
        self.messages = 0
        self.active = True 


class CacUserData(Base):
    __tablename__ = "cac_userdata"
    user_id = Column(Integer, primary_key=True)
    chosen_region_name = Column(String)
    chosen_street_name = Column(String)
    house_info1 = Column(String)
    house_info2 = Column(String)
    number_of_rooms = Column(Integer)
    cac_age = Column(Integer)
    area = Column(Float)
    price_of_finishing = Column(String)
    repair_coef = Column(Float)
    furniture_cost = Column(Integer)



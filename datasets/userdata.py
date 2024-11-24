from sqlalchemy import Column, Integer, String, Float, TextClause, text
from utils.data import UserData
import re, pandas as pd
from datasets.database import Session, Base

class CacUserData(Base):
    __tablename__ = "cac_userdata"
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(String, unique=True)
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


    def __load_region_street_data(self, query:TextClause) -> list:
        with Session() as session:
            rows = session.execute(query).fetchall()
        strings = [row[0] for row in rows]
        lists = [re.findall(r'\d+', string) for string in strings]
        lists = [[int(num) for num in lst] for lst in lists]
        comp_list = []
        for lst in lists:
            comp_list.extend(lst)
        for value in comp_list[:]:
            if value > 3500 or value < 600:
                comp_list.remove(value)
        return comp_list

    def find_region_deals(self, user_data:UserData) -> list:
        query = text(f"SELECT deals FROM regions{user_data.number_of_rooms} \
            WHERE region_name = '{user_data.chosen_region_name}'")
        return self.__load_region_street_data(query)


    def find_street_deals(self, user_data:UserData) -> list:
        query = text(f"SELECT deals FROM streets{user_data.number_of_rooms} \
            WHERE street_name = '{user_data.chosen_street_name}'")
        return self.__load_region_street_data(query)


    def add_user_data_to_database(self, user_id:int, user_data:UserData) -> None:
        with Session() as session:
            user = session.query(CacUserData).filter_by(user_id=user_id).first()
            user.furniture_cost = user_data.furniture_cost
            user.repair_coef = user_data.repair_coef
            user.area = user_data.area
            user.chosen_region_name = user_data.chosen_region_name
            user.chosen_street_name = user_data.chosen_street_name
            user.house_info1 = user_data.house_info1
            user.house_info2 = user_data.house_info2        
            user.cac_age = user_data.cac_age
            user.number_of_rooms = user_data.number_of_rooms
            user.price_of_finishing = user_data.price_of_finishing


    def get_user_data_from_db(self, user_id:int) -> dict:
        with Session() as session:
            user = session.query(CacUserData).filter(CacUserData.user_id == user_id).one()
            return UserData(
                chosen_region_name = user.chosen_region_name,
                chosen_street_name = user.chosen_street_name,
                house_info1 = user.house_info1,
                house_info2 = user.house_info2,
                number_of_rooms = user.number_of_rooms,
                cac_age = user.cac_age,
                area = user.area,
                price_of_finishing = user.price_of_finishing,
                repair_coef = user.repair_coef,
                furniture_cost = user.furniture_cost
            )

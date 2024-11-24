from sqlalchemy import Column, Integer, String
import re
from datasets.database import Session, Base


class StreetName(Base):
    __tablename__ = 'street_names'
    id = Column(Integer, primary_key=True)
    street_name = Column(String, unique=True)

    def street_names(self, chozen_street_name:str, return_all:bool=False) -> list[str]:
        with Session() as session:
            street_names = session.query(StreetName).all()
            if return_all:
                return street_names
        return [street for street in street_names if re.search(chozen_street_name, street, re.IGNORECASE)]
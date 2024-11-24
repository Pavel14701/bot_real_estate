from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from datasets.database import Session, Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(String, unique=True)
    chat_id =  Column(String)
    first_name = Column(String)
    last_name = Column(String)
    start_time = Column(DateTime)
    last_update = Column(DateTime)
    messages = Column(Integer)
    active = Column(Boolean)

    def add_user_to_base(self, user_data:dict) -> None:
        with Session() as session:
            new_user = User(
                chat_id=user_data['chat_id'],
                user_id=user_data['user_id'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                start_time=user_data['timestamp'],
                last_update=user_data['timestamp']
            )
            session.add(new_user)

    def update_messages(self, new_message_count:int) -> None:
        with Session() as session:
            self.messages = new_message_count
            self.last_update = datetime.now()

    def update_active_status(self, new_status:bool) -> None:
        with Session():
            self.active = new_status
            self.last_update = datetime.now()

    def return_all_users(self) -> list['User']:
        with Session() as session:
            return session.query(User).all()

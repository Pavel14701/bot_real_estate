import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, DeclarativeMeta, sessionmaker
from utils.utils import logger
import traceback

def create_tables(Base:DeclarativeMeta) -> None:
    engine = create_engine(os.getenv('DATABASE_URI'))
    Base.metadata.create_all(engine)


class Session:
    def __init__(self):
        self.engine = create_engine(os.getenv('DATABASE_URI'), pool_size=10, max_overflow=20)
        self.Session = sessionmaker(bind=self.engine)

    def __enter__(self):
        self._session = self.Session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is None:
                self.commit()
            else:
                logger.error("Exception occurred: %s", exc_val, exc_info=True)
                traceback_str = ''.join(traceback.format_tb(exc_tb))
                logger.error("Traceback: %s", traceback_str)
                self.rollback()
        finally:
            self.close()

    def commit(self):
        try:
            self._session.commit()
        except Exception as e:
            logger.error("Commit failed: %s", e, exc_info=True)
            self.rollback()
            raise

    def rollback(self):
        self._session.rollback()

    def close(self):
        self._session.close()
        self.engine.dispose()


Base = declarative_base()
create_tables(Base)
load_dotenv()

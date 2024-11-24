import re, os
from sqlalchemy import MetaData, Table, Column, Text, create_engine, inspect
from sqlalchemy.orm import sessionmaker
from datasets.streetname import StreetName
from datasets.user import User
from datasets.userdata import CacUserData
from datasets.regions import RegionsTables
from datasets.streets import StreetsTables 

class DataMigration:
    source_engine = create_engine(os.getenv('DATABASE_SORCE'))
    target_engine = create_engine(os.getenv('DATABASE_MAIN'))
    SourceSession = sessionmaker(bind=source_engine)
    TargetSession = sessionmaker(bind=target_engine)
    source_session = SourceSession()
    target_session = TargetSession()
    source_metadata = MetaData()
    target_metadata = MetaData()
    source_metadata.reflect(bind=source_engine)
    tables_to_migrate = [
        'regions0', 'regions1', 'regions2', 'regions3', 'regions4', 'regions5',
        'streets0', 'streets1', 'streets2', 'streets3', 'streets4', 'streets5',
        'street_names', 'users', 'cac_userdata'
    ]

    def __table_check(self, table_name:str) -> Table:
        if re.match('regions', table_name):
            return RegionsTables().regions1.__table__
        elif re.match('streets', table_name):
            return StreetsTables().streets1.__table__
        elif table_name == 'street_names':
            return StreetName.__table__
        elif table_name == 'users':
            return User.__table__
        elif table_name == 'cac_userdata':
            return CacUserData.__table__

    def __migrate_table(self, table_name:str) -> None:
        source_table = Table(table_name, self.source_metadata, autoload_with=self.source_engine)
        target_table = self.__table_check(table_name)
        inspector = inspect(self.target_engine)
        if not inspector.has_table(table_name):
            print(f"Creating table {table_name} in target database.")
            target_table.create(self.target_engine)
        else:
            print(f"Table {table_name} already exists in target database.")
        data = self.source_session.query(source_table).all()
        for row in data:
            insert_stmt = target_table.insert().values(**row._asdict())
            self.target_session.execute(insert_stmt)
        self.target_session.commit()
        print(f'Data migrated for table {table_name}.')

    def migration(self) -> None:
        for table_name in self.tables_to_migrate:
            try:
                self.__migrate_table(table_name)
            except Exception as e:
                print(e)
        self.source_session.close()
        self.target_session.close()    
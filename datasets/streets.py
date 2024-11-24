import pandas as pd
from sqlalchemy import Table, Column, Text, MetaData

class DynamicTables:
    def __init__(self):
        self.metadata = MetaData()
        self.tables = {}
        for i in range(6):
            table_name = f'streets{i}'
            table = Table(
                table_name, self.metadata,
                Column('street_name', Text),
                Column('deals', Text)
            )
            self.tables[table_name] = table


class StreetsTables:
    dynamic_tables=DynamicTables()

    def __init__(self):
        self.streets0 = self.dynamic_tables.tables['streets0']
        self.streets1 = self.dynamic_tables.tables['streets1']
        self.streets2 = self.dynamic_tables.tables['streets2']
        self.streets3 = self.dynamic_tables.tables['streets3']
        self.streets4 = self.dynamic_tables.tables['streets4']
        self.streets5 = self.dynamic_tables.tables['streets5']

    def save_street_data(self, data:pd.DataFrame, street:str, rooms:int|str) -> None:
        pass

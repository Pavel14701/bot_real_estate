import pandas as pd
from sqlalchemy import Table, Column, Text, MetaData


class DynamicTables:
    def __init__(self):
        self.metadata = MetaData()
        self.tables = {}
        for i in range(6):
            table_name = f'regions{i}'
            table = Table(
                table_name, self.metadata,
                Column('region_name', Text),
                Column('deals', Text)
            )
            self.tables[table_name] = table


class RegionsTables:
    dynamic_tables=DynamicTables()
    
    def __init__(self):
        self.regions0 = self.dynamic_tables.tables['regions0']
        self.regions1 = self.dynamic_tables.tables['regions1']
        self.regions2 = self.dynamic_tables.tables['regions2']
        self.regions3 = self.dynamic_tables.tables['regions3']
        self.regions4 = self.dynamic_tables.tables['regions4']
        self.regions5 = self.dynamic_tables.tables['regions5']

    def save_region_data(self, data:pd.DataFrame, region:str, rooms:int|str) -> None:
        pass

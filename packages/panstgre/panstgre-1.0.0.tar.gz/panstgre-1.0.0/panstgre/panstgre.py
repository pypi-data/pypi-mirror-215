import psycopg2
from psycopg2 import extras
import pandas as pd

class DataBase:
    def __init__(self,user:str,host:str,port:str,database:str,password:str,sche:str='public'):
        self.user,self.host,self.port,self.database,self.password = user,host,port,database,password
        self.sche : str = sche
        self.isOpen : bool = False

    def __str__(self):
        return f"{self.user}.{self.sche}"

    def connect(self):
        self.conn = psycopg2.connect(database=self.database,user=self.user,password=self.password,host=self.host,port=self.port)
        self.isOpen = True
        return self.conn.cursor()

    def tables(self) -> list[str]:
        cur = self.connect()
        cur.execute(f"SELECT tablename FROM pg_tables WHERE schemaname = '{self.sche}';")
        _tables = [x[0] for x in cur.fetchall()]
        cur.close()
        return _tables

    def close(self):
        self.conn.close()
        self.isOpen = False

    def commit(self):
        self.conn.commit()


class Table:
    def __init__(self,database:DataBase,tablename:str):
        self.database : DataBase = database
        self.name : str = tablename

    def __str__(self):
        return f"{str(self.database)}.{self.name}"
    
    def columns(self) -> dict[str,str]:
        cur = self.database.connect()
        cur.execute(f"SELECT COLUMN_NAME,data_type FROM information_schema.COLUMNS WHERE table_schema = '{self.database.sche}' AND TABLE_NAME = '{self.name}'")
        _columns = {k:v for k,v in cur.fetchall()}
        cur.close()
        return _columns
    
    def keys(self) -> list[str]:
        cur = self.database.connect()
        cur.execute(f"SELECT a.attname FROM pg_index i JOIN pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey) WHERE i.indrelid = '{self.name}'::regclass AND i.indisprimary")
        _keys = [x[0] for x in cur.fetchall()]
        cur.close()
        return _keys

class Panstgre:
    def __init__(self,table:Table):
        self.table : Table = table
        self.keys : list = table.keys()
        self.columns : dict[str,str] = table.columns()
        self.colnames : list = list(table.columns().keys())

    def read(self,query:str="")->pd.DataFrame:
        cur = self.table.database.conn.cursor()
        q = f"SELECT * FROM {self.table}" if query == "" else query
        cur.execute(q)
        df = pd.DataFrame(cur.fetchall(),columns=self.colnames,dtype=object)
        cur.close()
        return df

    def upset(self,df:pd.DataFrame):
        cur = self.table.database.conn.cursor()
        upcols = self.colnames.copy()
        for col in self.keys : upcols.remove(col)
        q = f"INSERT INTO {self.table} ({','.join(self.colnames)}) VALUES %s ON CONFLICT ({','.join(self.keys)}) DO UPDATE SET {','.join([f'{x} = EXCLUDED.{x}' for x in upcols])}"
        df.drop_duplicates(subset=self.keys,inplace=True)
        extras.execute_values(cur,q,df[self.colnames].values)
        cur.close()

import requests
from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

BASE = declarative_base()

class WeatherTables(BASE):
    __tablename__ = 'weather_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    dt = Column(Integer)
    cod = Column(Integer)
    city = Column(String)
    temperature = Column(Float)


class PostgresDB(object):

    _DB_HOST = 'containers-us-west-205.railway.app'
    _DB_USERNAME = 'postgres'
    _DB_PORT = '5622'
    _DB_DATABASE = 'railway'
    _ENGINE = None
    IS_CREATED = None
   
    @property
    def _get_db_password(self):
        db_pass = os.environ.get('DB_PASS', None)
        return db_pass
      

    def _get_connection(self):
        if self.IS_CREATED:
            self._connect()         
        else:
            self._connect()
            self._create_data_table()
            

    def _connect(self):
        try:
            db_pass = self._get_db_password
            connection = f'postgresql://{self._DB_USERNAME}:{db_pass}@{self._DB_HOST}:{self._DB_PORT}/{self._DB_DATABASE}'
            engine = create_engine(connection)
            self._ENGINE = engine
        except Exception as e:
            raise e
        
    def _create_data_table(self):
        try:
            BASE.metadata.create_all(self._ENGINE)
            self.IS_CREATED = True    
        except Exception as e:
            raise e
    
    def get_engine(self):
        if not self._ENGINE:
            self._get_connection()
        return self._ENGINE
    
    def get_session(self):
        self._get_connection()
        try:
            Session = sessionmaker(bind=self._ENGINE)
            session = Session()
            return session
        except Exception as e:
            raise e





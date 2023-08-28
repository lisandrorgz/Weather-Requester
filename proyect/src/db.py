import requests
from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

BASE = declarative_base()

"""
WeatherTables: Esta clase define una tabla weather_data en la base de datos con columnas id, dt, cod, city y temp. 
Utiliza la herencia de la clase declarative_base para definir la estructura de la tabla de manera declarativa.

"""
class WeatherTables(BASE):
    __tablename__ = 'weather_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    dt = Column(Integer)
    cod = Column(Integer)
    city = Column(String)
    temp = Column(Float)

"""
PostgresDB: Esta clase maneja la conexión a la base de datos PostgreSQL 
Proporciona métodos para obtener el motor de la base de datos y sesiones.
"""
class PostgresDB(object):

    _DB_HOST = 'containers-us-west-205.railway.app'
    _DB_USERNAME = 'postgres'
    _DB_PORT = '5622'
    _DB_DATABASE = 'railway'
    _ENGINE = None
    IS_CREATED = None
   
   # Método que obtiene la contraseña de la base de datos desde una variable de entorno (DB_PASS)
    @property
    def _get_db_password(self):
        db_pass = os.environ.get('DB_PASS', None)
        return db_pass
   
    #  Método que maneja la lógica de conexión a la base de datos. Si la conexión ya está creada, simplemente la devuelve. Si no, crea la conexión y llama al método _create_data_table.
    def _get_connection(self):
        if self.IS_CREATED:
            self._connect()         
        else:
            self._connect()
            self._create_data_table()

    #  Método que crea la conexión al motor de la base de datos utilizando SQLAlchemy.  
    def _connect(self):
        try:
            db_pass = self._get_db_password
            connection = f'postgresql://{self._DB_USERNAME}:{db_pass}@{self._DB_HOST}:{self._DB_PORT}/{self._DB_DATABASE}'
            engine = create_engine(connection)
            self._ENGINE = engine
        except Exception as e:
            raise e
        
    #  Método que crea la tabla en la base de datos utilizando el modelo definido en la clase WeatherTables
    def _create_data_table(self):
        try:
            BASE.metadata.create_all(self._ENGINE)
            self.IS_CREATED = True    
        except Exception as e:
            raise e
    
    #  Método para obtener el motor de la base de datos. Si el motor no existe, llama a _get_connection para crearlo.
    def get_engine(self):
        if not self._ENGINE:
            self._get_connection()
        return self._ENGINE
    
    # get_session: Método para obtener una sesión de la base de datos. Llama a _get_connection para asegurarse de que la conexión y la tabla están creadas, y luego crea y devuelve una sesión.
    def get_session(self):
        self._get_connection()
        try:
            Session = sessionmaker(bind=self._ENGINE)
            session = Session()
            return session
        except Exception as e:
            raise e





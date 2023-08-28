import os
import json
import datetime
from serializer import RequesterSerializer
from db import *
from algorithms.queue import ArrayQueue


class ExportAPIData(object):

    _CSV_CONT = 0
    _CONFIG_FILE = 'config.json'
    _CSV_DIR = 'data_analytics/openweather/tiempodiario'
    _DATABASE = PostgresDB()
        
    @classmethod
    def to_postgres(self, df):
        # OPCION 1: Exportar con pandas
        table_name = WeatherTables.__tablename__
        engine = self._DATABASE.get_engine()
        with engine.connect() as connection:
            df.to_sql(table_name, con=connection, if_exists='append', index=False)
     
        """

        OPCION 2: Exportar con SQLALCHEMY

        session = database.get_session()
        
        for data in data_list:
            dt = data['dt']
            cod = data['cod']
            city = data['city'] 
            temperature = data['temperature']
            record = WeatherTables(dt=dt, cod=cod, city=city, temperature=temperature)
            session.add(record)
        
        session.commit()
        session.close()
        """

    @classmethod
    def to_csv(cls, df, five_days=None):
        try:
            if not os.path.exists(cls.csv_dir):
                os.makedirs(cls.csv_dir)

            # Cargar el valor actual de csv_cont desde el archivo de configuración
            cls._load_csv_cont()
            cls._CSV_CONT += 1
            # Obtiene la fecha del dataframe y le agrega un identificador único csv_cont teniendo en cuenta el endpoint
            date_name = cls.get_date(
                df) + str(cls._CSV_CONT) + '.csv'
            completed_dir = os.path.join(cls.csv_dir, date_name)
            df.to_csv(completed_dir, index=False)
            # Guardar el nuevo valor de csv_cont en el archivo de configuración
            cls._save_csv_cont()
        except Exception as e:
            cls._CSV_CONT -= 1
            raise f'Ocurrió un error {e}'
    
    # Funcion que transforma a el formato 'yyy/mm/dd según la fecha por segundos del campo 'dt' del df
    @classmethod
    def get_date(cls, df):
        timestamp =  df['dt'].iloc[0]
        date = str(datetime.datetime.fromtimestamp(timestamp)).split(' ')[0]
        only_str = ''.join(date).replace('-', '')
        return only_str

    @classmethod
    def _load_csv_cont(cls):
        if os.path.exists(cls._CONFIG_FILE):
            with open(cls._CONFIG_FILE, 'r') as config_file:
                config = json.load(config_file)
                cls._CSV_CONT = config.get('csv_cont', 0)

    @classmethod
    def _save_csv_cont(cls):
        config = {'csv_cont': cls._CSV_CONT}
        with open(cls._CONFIG_FILE, 'w') as config_file:
            json.dump(config, config_file)

    @classmethod
    def _reset_cont(cls, cont_name):
        if cont_name == 'csv_cont':
            cls._CSV_CONT = 0
            cls._save_csv_cont()

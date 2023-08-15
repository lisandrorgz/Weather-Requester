import os
import json
import datetime
from serializer import RequesterSerializer
from db import *


class ExportAPIData(object):
    csv_cont = 0
    config_file = 'config.json'
    csv_dir = 'data_analytics/openweather/tiempodiario'

        
    @classmethod
    def to_postgres(self, df):
        # OPCION 1: Exportar con pandas
        
        database = PostgresDB()
        table_name = WeatherTables.__tablename__
        engine = database.get_engine()
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
            cls.load_csv_cont()
            cls.csv_cont += 1
            # Obtiene la fecha del dataframe y le agrega un identificador único csv_cont teniendo en cuenta el endpoint
            date_name = cls.get_date(
                df) + str(cls.csv_cont) + '.csv'
            completed_dir = os.path.join(cls.csv_dir, date_name)
            df.to_csv(completed_dir, index=False)
            # Guardar el nuevo valor de csv_cont en el archivo de configuración
            cls.save_csv_cont()
        except Exception as e:
            cls.csv_cont -= 1
            raise f'Ocurrió un error {e}'

    # Funciones del json de configuració, necesarias para resetear el contador unico de archivos
    @classmethod
    # Funcion que transforma a el formato 'yyy/mm/dd según la fecha por segundos del campo 'dt' del df
    def get_date(cls, df):
        timestamp =  df['dt'].iloc[0]
        date = str(datetime.datetime.fromtimestamp(timestamp)).split(' ')[0]
        only_str = ''.join(date).replace('-', '')
        return only_str

    @classmethod
    def load_csv_cont(cls):
        if os.path.exists(cls.config_file):
            with open(cls.config_file, 'r') as config_file:
                config = json.load(config_file)
                cls.csv_cont = config.get('csv_cont', 0)

    @classmethod
    def save_csv_cont(cls):
        config = {'csv_cont': cls.csv_cont}
        with open(cls.config_file, 'w') as config_file:
            json.dump(config, config_file)

    @classmethod
    def reset_cont(cls, cont_name):
        if cont_name == 'csv_cont':
            cls.csv_cont = 0
            cls.save_csv_cont()

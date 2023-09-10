import os
import json
import datetime
from .db import *
from .queue import ArrayQueueM
import pandas as pd 


class ExportAPIData(object):

    _DATABASE = PostgresDB()
    _QUEUE = ArrayQueueM()
     
    def to_postgres(self):
        # OPCION 1: Exportar con pandas
        table_name = WeatherTables.__tablename__
        engine = self._DATABASE.get_engine()
        with engine.connect() as connection:
            master_df = self._dequeue_pandas()
            master_df.to_sql(table_name, con=connection, if_exists='append', index=False)
     
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

    def to_csv(self):
        prox_df = self._QUEUE.array
        dircc = prox_df.completed_dir
        print(dircc)
        master_df_csv = self._dequeue_pandas()  
        master_df_csv.to_csv(dircc, index=False)
    
    def _dequeue_pandas(self):
        df = None
        while not self._QUEUE.is_empty():
            parcial_df = self._QUEUE.dequeue()
            df = parcial_df if df is None else pd.concat([df, parcial_df])
        return df

    
    # Funcion que transforma a el formato 'yyy/mm/dd según la fecha por segundos del campo 'dt' del df
    
    


   
    
   


  


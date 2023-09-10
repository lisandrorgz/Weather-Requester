import pandas as pd 
import json
import os
from geopy.geocoders import Nominatim
import datetime

class RequesterSerializer(object):

    _CSV_CONT = 0
    _CONFIG_FILE = 'config.json'
    _CSV_DIR = 'data_analytics/openweather/tiempodiario'


    def json_to_df_csv(self, json):
        df = self.normalize_to_df(json)
        try:
            if not os.path.exists(self._CSV_DIR):
                os.makedirs(self._CSV_DIR)
            # Cargar el valor actual de csv_cont desde el archivo de configuración
            self._load_csv_cont()
            self._CSV_CONT += 1
            # Obtiene la fecha del dataframe y le agrega un identificador único csv_cont teniendo en cuenta el endpoint
            date_name = self._get_date(
                df) + str(self._CSV_CONT) + '.csv'
            completed_dir = os.path.join(self._CSV_DIR, date_name)
            #df.to_csv(completed_dir, index=False)
            df.completed_dir = completed_dir
            # Guardar el nuevo valor de csv_cont en el archivo de configuración
            self._save_csv_cont()
            
        except Exception as e:
            self._CSV_CONT -= 1
            raise f'Ocurrió un error en la carga de archivos csv {e}'
        return df
    

    def json_to_df_postgres(self, json):
        # OPCIÓN 1: DEVOLVER DF PARA EXPORTAR CON PANDAS
        df = self.normalize_to_df(json, True)
        df['city'] = df['city'].apply(lambda x: x['name'])
        df = df[['dt', 'cod', 'city','main.temp']].rename(columns={'main.temp': 'temp', 'city':'city'})
        return df
        """
        # OPCIÓN 2: TRANSFORMAR DF PARA EXPORTAR CON SQLALCHEMY
        df_main = pd.DataFrame(df['main.temp'].apply(pd.Series))
        list_of_days = []
        city = df.loc[0, 'city']['name']
        for i in range(1, len(df)):
            dt = int(df.loc[i, 'dt'])
            cod = df.loc[i, 'cod']
            temperature = int(df_main.iloc[i])
            list_of_days.append({'city':city,'dt':dt, 'cod':cod, 'temperature':temperature})
        return df_nested
        """         

    def normalize_to_df(self, json, five_days=None):
        try:
            df = pd.json_normalize(json, record_path='list', meta=['city','cod']) if five_days else pd.json_normalize(json)
        except pd.json_normalize.JSONDecodeError as e:
            raise ValueError("Error al decodificar el JSON proporcionado") from e
        return df
        
    
    def elem_list_to_a_dicc(self, element, api_key):
        dicc = {}
        params = element.split('&')  
        for elem in params:
            key, value = elem.split('=')
            dicc[key] = value
        dicc['appid'] = api_key
        return dicc

    def get_coord(self, city):
        # Si se pasa una ciudad como parametro, la funcion devuelve sus coordenadas
        geolocator = Nominatim(user_agent="weather_app")  
        location = geolocator.geocode(city)
        if location:
            latitud = location.latitude
            longitud = location.longitude
            return f'lat={latitud}&lon={longitud}'
        print(f"\nNo se pudieron obtener las coordenadas para {city}.")
        return None
    
    def _load_csv_cont(self):
        if os.path.exists(self._CONFIG_FILE):
            with open(self._CONFIG_FILE, 'r') as config_file:
                config = json.load(config_file)
                self._CSV_CONT = config.get('csv_cont', 0)

   
    def _save_csv_cont(self):
        config = {'csv_cont': self._CSV_CONT}
        with open(self._CONFIG_FILE, 'w') as config_file:
            json.dump(config, config_file)


    def _reset_cont(self, cont_name):
        if cont_name == 'csv_cont':
            self._CSV_CONT = 0
            self._save_csv_cont()

    def _get_date(self, df):
        timestamp =  df['dt'].iloc[0]
        date = str(datetime.datetime.fromtimestamp(timestamp)).split(' ')[0]
        only_str = ''.join(date).replace('-', '')
        return only_str
    

    
 
    

        
        

        



    

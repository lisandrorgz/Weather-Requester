import pandas as pd 
import json

class RequesterSerializer(object):
    
    @classmethod
    def json_to_df_csv(cls, json):
        df = cls.normalize_to_df(json)
        return df
    
    @classmethod
    def json_to_df_postgres(cls, json):
        # OPCIÓN 1: DEVOLVER DF PARA EXPORTAR CON PANDAS
        df = cls.normalize_to_df(json, True)
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
            
            

    @classmethod
    def normalize_to_df(cls, json, five_days=None):
        try:
            df = pd.json_normalize(json, record_path='list', meta=['city','cod']) if five_days else pd.json_normalize(json)
        except pd.json_normalize.JSONDecodeError as e:
            raise ValueError("Error al decodificar el JSON proporcionado") from e
        return df
        
    
    
    @classmethod
    def elem_list_to_a_dicc(cls, element, api_key):
        dicc = {}
        params = element.split('&')  
        for elem in params:
            key, value = elem.split('=')
            dicc[key] = value
        dicc['appid'] = api_key
        return dicc
    
 
    

        
        

        



    

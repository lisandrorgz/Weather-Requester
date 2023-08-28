import requests
from serializer import RequesterSerializer
from export import ExportAPIData
from geopy.geocoders import Nominatim
import os

# ApiRequester es una clase que maneja las solicitudes a la API de OpenWeather
class ApiRequester(object):

    # url_one_day y url_five_days son las URLs de los endpoints para obtener datos climáticos para un día o cinco días, respectivamente.
    __URL_ONE_DAY = 'https://api.openweathermap.org/data/2.5/weather?'
    __URL_FIVE_DAYS = 'https://api.openweathermap.org/data/2.5/forecast?'

    def __init__(self, param_list=None):
        self.__api_key = None
        self.param_list = param_list

    @property
    def api_key(self):
        return self._api_key
    
    @api_key.setter
    def api_key(self, value):
        self._api_key = value
    
    def set_requester_api_key(self):
        try:
            api_key = os.environ.get('WEATHER_APP', None)
            if api_key is None:
                raise ValueError('API Key no encontrada en la variable de entorno')
            self.api_key = api_key
        except:
            raise ImportError('Error al buscar la api key')

        
    # make_requests: Este método realiza las solicitudes a la API. Puede hacer solicitudes para un solo día o cinco días, dependiendo del valor de five_days.
    def make_requests(self, five_days=None):

        if self._api_key:
            if self.param_list is not None:
                # Se guarda el largo del array en el algoritmo cola
                how_much_elements = len(self.param_list)
                RequesterSerializer.QUEUE.queue_lenght = how_much_elements    
                # Itera segun la cantidad de elementos en param_list, por cada uno hace una request
                # Si solo se le pasa el nombre de una ciudad como parametro, el codigo lo reconoce y hace la petición al respectivo endpoint
                # Pero si solo se le pasa parametros, el codigo lo reconoce y hace la petición al respectivo endpoint
                param = ''
                for element in self.param_list:
                     # Obtiene los parametros geograficos si el elemento es el nombre de una ciudad, si no, el mismo elemento
                    param = self.get_coord(element) if '=' not in element else element 
                    if param is not None:
                        try:
                            dicc_params = RequesterSerializer.elem_list_to_a_dicc(param, self.api_key)
                            response = requests.get(self.url_one_day, params=dicc_params) if not five_days else requests.get(self.url_five_days, params=dicc_params) 
                        except requests.exceptions.RequestException as e:           
                                return f"Ocurrió un error {e}"
                                    
                        finally:
                                print(f"\nRequest con parametros: {element}\nCódigo de estado: {response.status_code}")
                                        
                        # Si ld data ha sido enviada, se la normaliza y se la exporta, si no, muestra el status_code.
                        self.process_response(response, five_days = five_days)
                                    
            else:
                print("No se ingresaron parametros al Requester\nSaliendo...")
                return None
        else:
             print("No se suministro una api key\nSaliendo...")
             return None

     #Este método procesa la respuesta de la API. Si el código de estado es 200 (éxito), convierte la respuesta JSON en un DataFrame utilizando RequesterSerializer 
     #Lo exporta a CSV o a una base de datos PostgreSQL, según la configuración. 
               
    @classmethod
    def process_response(cls, response, five_days):
        
        if response.status_code == 200:
                    r_json = response.json()
                    if five_days:   
                         df = RequesterSerializer.json_to_df_postgres(r_json)
                         if df is not None:
                            ExportAPIData.to_postgres(df)
                    else:
                        df = RequesterSerializer.json_to_df_csv(r_json)
                        if df is not None:
                            ExportAPIData.to_csv(df)
                        


    @classmethod
    def get_coord(cls, city):
        # Si se pasa una ciudad como parametro, la funcion devuelve sus coordenadas
        geolocator = Nominatim(user_agent="weather_app")  
        location = geolocator.geocode(city)
        if location:
            latitud = location.latitude
            longitud = location.longitude
            return f'lat={latitud}&lon={longitud}'
        else:
            print(f"\nNo se pudieron obtener las coordenadas para {city}.")
        return None
    


        










    
    




    
        


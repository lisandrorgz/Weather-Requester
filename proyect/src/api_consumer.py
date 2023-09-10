from .export import ExportAPIData
from .serializer import RequesterSerializer
import os
import requests

# ApiRequester es una clase que maneja las solicitudes a la API de OpenWeather
class ApiRequester(object):

    # url_one_day y url_five_days son las URLs de los endpoints para obtener datos climáticos para un día o cinco días, respectivamente.
    _URL_ONE_DAY = 'https://api.openweathermap.org/data/2.5/weather?'
    _URL_FIVE_DAYS = 'https://api.openweathermap.org/data/2.5/forecast?'
    _SERIALIZER = RequesterSerializer()
    _EXPORT = ExportAPIData()

    def __init__(self, param_list, five_days=None):
        if param_list is None and not isinstance(param_list, int):
            return ValueError('Valor "param_list" inválido')
        self._api_key = None
        self._five_days = five_days
        self._size = len(param_list)  
        self._param_list = param_list
        self._EXPORT._QUEUE.array = self._size
    
    @property
    def api_key(self):
        return self._api_key
    
    @api_key.setter
    def api_key(self, value):
        self._api_key = value

    
    def set_requester_api_key(self):
        api_key = os.environ.get('WEATHER_APP', None)
        if api_key is None:
            return ImportError('API Key no encontrada en la variable de entorno')
        self.api_key = api_key


        
    # make_requests: Este método realiza las solicitudes a la API. Puede hacer solicitudes para un solo día o cinco días, dependiendo del valor de five_days.
    def make_requests(self):
        if self._api_key:
                # Se guarda el largo del array en el algoritmo cola   
                # Itera segun la cantidad de elementos en param_list, por cada uno hace una request
                # Si solo se le pasa el nombre de una ciudad como parametro, el codigo lo reconoce y hace la petición al respectivo endpoint
                # Pero si solo se le pasa parametros, el codigo lo reconoce y hace la petición al respectivo endpoint
                for element in self._param_list:
                     # Obtiene los parametros geograficos si el elemento es el nombre de una ciudad, si no, el mismo elemento
                    param = self._SERIALIZER.get_coord(element) if '=' not in element else element 
                    if param is not None:
                        try:
                            dicc_params = self._SERIALIZER.elem_list_to_a_dicc(param, self.api_key)
                            response = requests.get(self._URL_ONE_DAY, params=dicc_params) if not self._five_days else requests.get(self._URL_FIVE_DAYS, params=dicc_params) 
                        except requests.exceptions.RequestException as e:           
                            return f"Ocurrió un error {e}"      
                        finally:
                                print(f"\nRequest con parametros: {element}\nCódigo de estado: {response.status_code}")
                                        
                        # Si ld data ha sido enviada, se la normaliza y se la exporta, si no, muestra el status_code.
                        self._process_response(response)
                    else:
                        raise ValueError(f"Valor incorrecto para {param}")

                self._EXPORT.to_postgres() if self._five_days else self._EXPORT.to_csv()


        else:
             print('Suministra "api_key" para utilizar la función\n')
             return None

     #Este método procesa la respuesta de la API. Si el código de estado es 200 (éxito), convierte la respuesta JSON en un DataFrame utilizando RequesterSerializer 
     #Lo exporta a CSV o a una base de datos PostgreSQL, según la configuración. 
                 
    def _process_response(self, response):
        if response.status_code == 200:
                    r_json = response.json()
                    if self._five_days:   
                        df = self._SERIALIZER.json_to_df_postgres(r_json)
                        self._EXPORT._QUEUE.enqueue(df) 
                            
                    else:
                        df = self._SERIALIZER.json_to_df_csv(r_json)
                        self._EXPORT._QUEUE.enqueue(df)
                            
        else:
            raise ValueError(f"status_code {response.status_code}")


        

                        


    

    


        










    
    




    
        


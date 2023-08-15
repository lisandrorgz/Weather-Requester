import sys
sys.path.append('../')
import unittest
from api_consumer import ApiRequester
from params import api_key

class TestApiRequester(unittest.TestCase):

    def setUp(self):
        self.api_key = api_key
        self.requester = ApiRequester()

    def test_make_requests_with_api_key(self):
        # Simula una llamada a la API con una clave de API válida
        self.requester.api_key = self.api_key
        self.requester.param_list = ['London', 'New York']
        result = self.requester.make_requests()

        # Afirmar que el resultado es None, ya que make_requests() no devuelve nada
        self.assertIsNone(result)



    def test_make_requests_without_api_key(self):
        # Simula una llamada a la API sin una clave de API
        self.requester.api_key = None
        self.requester.param_list = ['London', 'New York']
        result = self.requester.make_requests()

        # Afirmar que el resultado es None, ya que make_requests() no devuelve nada
        self.assertIsNone(result)



    def test_process_response_with_successful_response(self):
        # Simula una respuesta exitosa de la API
        response = {'status_code': 200, 'data': {'temp': 25, 'humidity': 50}}

        # Ejecutar el método process_response
        ApiRequester.process_response(response)

    def test_process_response_with_error_response(self):
        # Simula una respuesta de error de la API
        response = {'status_code': 404, 'data': {'message': 'Not Found'}}

        # Ejecutar el método process_response
        ApiRequester.process_response(response)



if __name__ == '__main__':
    unittest.main()

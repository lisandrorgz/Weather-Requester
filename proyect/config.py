from src.api_consumer import ApiRequester
from src.params import *

if __name__ == '__main__':
    requester = ApiRequester(all_parameters)
    requester.set_requester_api_key() 
    requester.make_requests()
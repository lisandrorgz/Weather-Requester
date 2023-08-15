from api_consumer import ApiRequester
from params import *

if __name__ == '__main__':
    requester = ApiRequester(all_parameters) 
    requester.api_key = api_key
    requester.make_requests(five_days=True)
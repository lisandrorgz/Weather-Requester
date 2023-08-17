from api_consumer import ApiRequester
from params import *

if __name__ == '__main__':
    requester = ApiRequester(all_parameters) 
    requester.make_requests(five_days=True)
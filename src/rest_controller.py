import falcon
import request_handler
import json
from datetime import datetime

class Price(object):
    def on_get(self, req, resp, timestamp): 
        resp.media = request_handler.get_current_prices(timestamp) 

        

        



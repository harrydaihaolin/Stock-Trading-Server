import falcon
import request_handler
import json

class Price(object):
    def on_get(self, req, resp): 
        resp.media = request_handler.get_stock_quote('AAPL') 

        

        



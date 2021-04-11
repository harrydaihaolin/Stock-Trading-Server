import falcon
import request_handler
import json
from datetime import datetime

class Price(object):
    def on_get(self, req, resp, timestamp): 
        resp.media = json.dumps(request_handler.get_current_prices(timestamp))

class AddTicker(object):
    def on_post(self, req, resp):
        ticker = req.get_param("value", required=True)
        request_handler.addAlphaTickerData(ticker, '5')

class DelTicker(object):
    def on_post(self, req, resp):
        ticker = req.get_param("value", required=True)
        request_handler.delAlphaTickerData(ticker)

        

        



import falcon
import request_handler
import json

class Price(object):
    def on_get(self, req, resp, timestamp): 
        resp.media = json.dumps(request_handler.get_current_prices(timestamp))

class AddTicker(object):
    def on_get(self, req, resp, ticker):
        request_handler.addAlphaTickerData(ticker)
        resp.media={'status': 'success'}

class DelTicker(object):
    def on_get(self, req, resp, ticker):
        request_handler.delAlphaTickerData(ticker)
        resp.media={'status': 'success'}

class Signal(object):
    def on_get(self, req, resp, timestamp):
        resp.media = json.dumps(request_handler.get_signal(timestamp))




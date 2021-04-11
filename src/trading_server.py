import logging
logging.basicConfig(level=logging.INFO)
import sys
import time
import constants
import request_handler
import sqlite_connector 
import falcon
import gunicorn.app.base
import multiprocessing
from server_argument_parser import parser
from rest_controller import Price

class TradingServer(gunicorn.app.base.BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1

def run(port=8000):
    options = {
        'bind': '{}:{}'.format('127.0.0.1', port),
        'workers': number_of_workers(),
    }
    api = falcon.API()
    api.add_route('/price', Price())
    TradingServer(api, options).run()


if __name__ == '__main__':
    logging.info('processing arguments...')
    args = parser.parse_args()
    # default interval is 5 minutes
    valid_minutes = '5' 
    # actions on argument 
    if (args.minutes):
        valid_minutes = request_handler.get_valid_minutes(args.minutes)
    if (args.tickers):
       # load and process csv files
       for ticker in args.tickers:
            request_handler.addAlphaTickerData(ticker, valid_minutes)
#    if (args.reload):
    sqlite_connector.load_data()
    if (args.interactive):
        request_handler.Shell().cmdloop(constants.WELCOME)
        sys.exit(0)
    if (args.port):
        run(args.port)
    else:
        run()
 


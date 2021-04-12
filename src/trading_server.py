from datetime import datetime
import logging
logging.basicConfig(filename="logs/server_log_{}.log".format(datetime.now(tz=None).strftime('%s')),level=logging.INFO)
import atexit
import sys
import constants
import request_handler
import sqlite_connector 
import falcon
import gunicorn.app.base
import multiprocessing
import mail
from os import walk
from server_argument_parser import parser
from rest_controller import Price, AddTicker, DelTicker

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
   return 2 * multiprocessing.cpu_count() + 1 

def run(port=8000):
    options = {
        'bind': '{}:{}'.format('127.0.0.1', port),
        'workers': number_of_workers(),
        'keepalive': 5
    }
    api = falcon.App()
    api.add_route('/price/{timestamp}', Price())
    api.add_route('/add_ticker/{ticker}', AddTicker())
    api.add_route('/del_ticker/{ticker}', DelTicker())
    try:
        TradingServer(api, options).run()
    except Exception as e:
        logging.error(e)

def exit_handler():
    logging.info("sending emails before shut down...")
    mail.send_mail()

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
       if (len(args.tickers) > 3):
           for i in range(0, 3):
               request_handler.addAlphaTickerData(args.tickers[i], valid_minutes)
       else:
           for ticker in args.tickers:
               request_handler.addAlphaTickerData(ticker, valid_minutes)
    if (args.reload):
        _, _, filenames = next(walk('out/'))
        for filename in filenames:
            if (filename == args.reload):
                request_handler.reload(filename)
    logging.info("loading sqlite data through connector..")
    if (args.interactive):
        request_handler.Shell().cmdloop(constants.WELCOME)
        sys.exit(0)
    atexit.register(exit_handler)
    request_handler.loadDataToDatabase()
    _, _, filenames = next(walk('out/'))
    load = True
    for filename in filenames:
        if ("result" in filename):
            load = False
    if load:
        request_handler.loadTradingStrategy()
    request_handler.loadDataToDatabase()
    if (args.port):
        run(args.port)
    else:
        run()

import logging
logging = logging.getLogger()
import constants
import sys
from datetime import datetime
import finnhub
import csv
import signal
import json
import sqlite_connector
from alpha_vantage.timeseries import TimeSeries
from cmd import Cmd
from os import walk, path

def addAlphaTickerData(ticker, interval): 
    try:
        ts = TimeSeries(key=constants.ALPHAADVANTAGEKEY, output_format='csv')
        logging.info("Getting intraday {} data from Alpha Vantage".format(ticker)) 
        data, _ = ts.get_intraday(symbol=ticker, interval=interval+'min', outputsize='full')

        logging.info("Generating {}.csv".format(ticker)) 
        with open('out/' + ticker + ".csv", 'w') as write_csvfile:
            writer = csv.writer(write_csvfile, dialect='excel')
            for row in data:
                writer.writerow(row)
        logging.info("Generation successful!")
    except KeyboardInterrupt():
        pass
    except Exception as e:
        logging.error(e)

def list_all_tickers():
    _, _, filenames = next(walk('out/'))
    return filenames

def get_stock_quote(ticker):
    try:
        finnhub_client = finnhub.Client(api_key=constants.FINNHUBKEY)
        res = finnhub_client.quote(ticker)
        return res
    except Exception as e:
        logging.error(e)

def get_valid_minutes(minutes):
   if (minutes == 15 or minutes == 30 or minutes == 60):
       return str(minutes)
   else:
       return '5'

def get_current_prices(date):
    tickers = {} 
    filenames = list_all_tickers()
    try:
        for filename in filenames:
            no_ext_name = path.splitext(filename)[0] 
            if (date == 'now'):
                price = sqlite_connector.get_latest_prices(no_ext_name)
            else:
                price = sqlite_connector.get_current_prices(date, no_ext_name)
            tickers[no_ext_name] = price 
        return tickers 
    except Exception as e:
        logging.error(e)

def reload(filename):
    sqlite_connector.reload_data(filename)

# interactive console for testing purposes
class Shell(Cmd):
    def cmdloop(self, intro):
        if intro is not None: print(intro)
        while True:
            try:
                super(Shell, self).cmdloop(intro="")
                break
            except KeyboardInterrupt:
                print("^C")
                break

    def do_exit(self, inp):
        print("Bye")
        return True

    def do_add_ticker(self, inp):
        print("Adding '{}'".format(inp))
        parser = inp.split(' ')
        if (len(parser) != 2):
            print("please put add_ticker $TICKER $MINUTES")
        else:
            addAlphaTickerData(parser[0], parser[1])

    def do_get_stock_quote(self, inp):
        print("Getting '{}'".format(inp))
        if (inp is None):
            print("please put get_stock_quote $TICKER")
        else:
            data = get_stock_quote(inp)
            print(json.dumps(data))

    def do_get_current_prices(self, inp):
        if (inp is None):
            print("please put get_current_prices $DATETIME")
        else:
            data = get_current_prices(int(inp))
            print(data)


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
import os

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

def delAlphaTickerData(ticker):
    try:
        logging.info("Delete Ticker data from the database")
        sqlite_connector.delete_ticker(ticker)
        filepath = "out/" + ticker + ".csv"
        if (os.path.exists("out/" + ticker + ".csv")):
            os.remove(filepath)
        else:
            print("The file does not exist")
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
                price = sqlite_connector.get_current_prices(int(date), no_ext_name)
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
            data = get_current_prices(inp)
            print(data)

    def do_reload(self, inp):
        if (inp is None):
            print("please put get_current_prices $DATETIME")
        else:
            reload(inp)
            
    def do_delete_ticker(self, inp):
        if (inp is None):
            print("please put delete_ticker $TICKER")
        else:
            delAlphaTickerData(inp)

    def do_list_all_tickers(self, inp):
        tickers = list_all_tickers()
        print(tickers)

           


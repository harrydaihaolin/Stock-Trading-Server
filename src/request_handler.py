import logging
logging = logging.getLogger()
import constants
import sys
from datetime import datetime
import finnhub
import statistics
import csv
import signal
import json
import sqlite_connector
import os
from alpha_vantage.timeseries import TimeSeries
from cmd import Cmd
from os import walk, path

def loadDataToDatabase():
    sqlite_connector.load_data()

def loadResultFile():
    _, _, filenames = next(walk('out/'))
    for filename in filenames:
        no_ext_name = path.splitext(filename)[0] 

def addAlphaTickerData(ticker, interval='5'): 
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

def get_signal(timestamp):
    tickers = {} 
    filenames = list_all_tickers()
    try:
        signal = 0
        for filename in filenames:
            no_ext_name = path.splitext(filename)[0] 
            if 'result' in no_ext_name:
                if (timestamp == 'now'):
                    signal = sqlite_connector.get_latest_signal(no_ext_name)
                else:
                    signal = sqlite_connector.get_signal(int(timestamp), no_ext_name)
                tickers[no_ext_name] = signal
        return tickers
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
            logging.info("The file does not exist")
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

def get_sigma(ticker):
    all_prices = sqlite_connector.get_sigma(ticker) 
    container = []
    for price in all_prices:
        container.append(float(price[0]))
    return statistics.stdev(container)

def get_avg(ticker):
    all_prices = sqlite_connector.get_sigma(ticker) 
    avg = 0.0
    for price in all_prices:
        avg=avg+float(price[0]) 
    return avg / len(all_prices)

def tradingStrategy(ticker):
    inp = []
    price_inp = []
    avg = 0.0
    rolling_data = sqlite_connector.get_rolling_data(ticker)
    if rolling_data is not None:
        container = []
        for rd in rolling_data:
            avg = avg + float(rd[1])
            container.append(float(rd[1]))
        if len(rolling_data) != 0:
            avg = avg / len(rolling_data)
        sigma = statistics.stdev(container)
        pnl = 0.0
        for i in range(1, len(rolling_data)):
            tmp=[]
            tmp.append(rolling_data[i][0]) # timestamp
            price = rolling_data[i][1]
            last_price = rolling_data[i-1][1]
            tmp.append(price)
            price_inp.append(tmp)
                
            if (float(price) > (avg + sigma)):
                tmp.append(1)
                pnl = float(price) - float(last_price) 
                tmp.append(pnl)
            elif (float(price) < (avg - sigma)):
                tmp.append(-1)
                pnl = float(last_price) - float(price)
                tmp.append(pnl)
            else:
                tmp.append(0)
                tmp.append(0)
            inp.append(tmp)

    logging.info("generating {}_result.csv".format(ticker))
    with open('out/{}_result.csv'.format(ticker), 'w') as write_csvfile:
        writer = csv.writer(write_csvfile, dialect='excel')
        for row in inp:
            writer.writerow(row)
    logging.info("generation successful")

    logging.info("generating {}_price.csv".format(ticker))
    with open('out/{}_price.csv'.format(ticker), 'w') as write_csvfile:
        writer = csv.writer(write_csvfile, dialect='excel')
        for row in price_inp:
            writer.writerow(row)
    logging.info("generation successful")

def loadTradingStrategy():
    _, _, filenames = next(walk('out/'))
    for filename in filenames:   
        no_ext_name = path.splitext(filename)[0] 
        tradingStrategy(no_ext_name)

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

    def do_get_sigma(self, inp):
        if (inp is None):
            print("please put get_sigma $TICKER")
        else:
            res = get_sigma(inp)
            print(res)
    
    def do_trading_strategy(self, inp):
        if (inp is None):
            print("please put trading_strategy $TICKER")
        else:
            tradingStrategy(inp)
           

    def do_get_signal(self, inp):
        if (inp is None):
            print("please put get_signal $TIMESTAMP")
        else:
            r = get_signal(inp)
            print(r)

    def do_get_rolling_data(self, inp):
        if (inp is None):
            print("please put get_rolling_data $TICKER")
        else:
            r = sqlite_connector.get_rolling_data(inp)
            print(r)

import logging
logging = logging.getLogger()
import sqlite3
import csv
import constants
from functools import reduce
from os import walk, path

def get_latest_signal(ticker):
    try:
        con = sqlite3.connect(constants.DATABASENAME)
        cur = con.cursor()
        cur.execute('SELECT signal from {} limit 1'.format(ticker))
        rows = cur.fetchall()
        con.close()
        return rows
    except Exception as e:
        logging.error(e)

def get_signal(date, ticker):
    try:
        con = sqlite3.connect(constants.DATABASENAME)
        cur = con.cursor()
        cur.execute('SELECT signal from {} where timestamp={}'.format(ticker, date))
        rows = cur.fetchall() 
        con.close()
        return rows
    except Exception as e:
        logging.error(e)

def get_rolling_data(ticker):
    try:
        con = sqlite3.connect(constants.DATABASENAME)
        cur = con.cursor()
        cur.execute('SELECT timestamp, close FROM {} LIMIT 160'.format(ticker))
        rolling_data = cur.fetchall()
        con.close()
        return rolling_data
    except Exception as e:
        logging.error(e)

def get_sigma(ticker):
    try:
        con = sqlite3.connect(constants.DATABASENAME)
        cur = con.cursor()
        # there are 160 timestamps within 24 hours
        cur.execute('SELECT close FROM {} LIMIT 160'.format(ticker))
        all_prices = cur.fetchall()
        con.close()
        return all_prices
    except Exception as e:
        logging.error(e)

def delete_ticker(ticker):
    try:
        con = sqlite3.connect(constants.DATABASENAME)
        cur = con.cursor()
        cur.execute('DROP TABLE {}'.format(ticker))
        con.commit()
        con.close()
    except Exception as e:
        logging.error(e)

def get_latest_prices(ticker):
    try:
        con = sqlite3.connect(constants.DATABASENAME)
        cur = con.cursor()
        cur.execute('SELECT close from {} limit 1'.format(ticker))
        rows = cur.fetchall() 
        con.close()
        return rows
    except Exception as e:
        logging.error(e)

def get_current_prices(date, ticker):
    try:
        con = sqlite3.connect(constants.DATABASENAME)
        cur = con.cursor()
        cur.execute('SELECT close from {} where timestamp={}'.format(ticker, date))
        rows = cur.fetchall()
        con.close()
        return rows
    except Exception as e:
        print(e)

def reload_data(filename):
    try:
        logging.info("reloading the data from {}".format(filename))
        con = sqlite3.connect(constants.DATABASENAME)
        cur = con.cursor()
        f = open("out/" + filename)
        rows = csv.reader(f)
        next(rows, None)
        no_ext_name = path.splitext(filename)[0]
        cur.execute("DROP TABLE {}".format(no_ext_name))
        if "price" in no_ext_name:
            cur.execute("CREATE TABLE {} (timestamp, price)".format(no_ext_name))
            cur.executemany("INSERT INTO {} VALUES (CAST(strftime('%s', ?) as integer), ?)", rows)
        elif "result" in no_ext_name:
            cur.execute("CREATE TABLE {} (timestamp, price, signal, pnl)".format(no_ext_name))
            cur.executemany("INSERT INTO {} VALUES (CAST(strftime('%s', ?) as integer), ?, ?, ?)", rows)
        else:
            cur.execute("CREATE TABLE {} (timestamp, open, high, low, close, volume)".format(no_ext_name))
            cur.executemany("INSERT INTO {} VALUES (CAST(strftime('%s', ?) as integer), ?, ?, ?, ?, ?)".format(no_ext_name), rows)
        con.commit()
        con.close()
        logging.info("data successfully loaded")
    except Exception as e:
        logging.error(e)

def load_data():
    # load the data when starting the server
    try:
        logging.info("loading the data to local database")
        con = sqlite3.connect(constants.DATABASENAME)
        cur = con.cursor()
        _, _, filenames = next(walk('out/'))
        for filename in filenames:
            f = open("out/" + filename) 
            rows = csv.reader(f)
            next(rows, None) # skip the headers
            no_ext_name = path.splitext(filename)[0] 
            if "price" in no_ext_name:
                cur.execute("CREATE TABLE {} (timestamp, price)".format(no_ext_name))
                cur.executemany("INSERT INTO {} VALUES (CAST(strftime('%s', ?) as integer), ?)", rows)
            elif "result" in no_ext_name:
                cur.execute("CREATE TABLE {} (timestamp, price, signal, pnl)".format(no_ext_name))
                cur.executemany("INSERT INTO {} VALUES (CAST(strftime('%s', ?) as integer), ?, ?, ?)", rows)
            else:
                cur.execute("CREATE TABLE {} (timestamp, open, high, low, close, volume)".format(no_ext_name))
                cur.executemany("INSERT INTO {} VALUES (CAST(strftime('%s', ?) as integer), ?, ?, ?, ?, ?)".format(no_ext_name), rows)
        con.commit()
        con.close()
        logging.info("data successfully loaded")
    except Exception as e:
        logging.error(e)

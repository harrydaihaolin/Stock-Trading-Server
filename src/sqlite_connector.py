import logging
logging = logging.getLogger()
import sqlite3
import csv
import constants
from os import walk, path

def get_current_prices(date, ticker):
    try:
        con = sqlite3.connect(constants.DATABASENAME)
        cur = con.cursor()
        cur.execute('SELECT close from {} where timestamp="{}"'.format(ticker, date))
        rows = cur.fetchall()
        con.close()
        return rows
    except Exception as e:
        print(e)

def load_data():
    # load the data when starting the server
    try:
        logging.info("loading the data to in-memory database")
        con = sqlite3.connect(constants.DATABASENAME)
        cur = con.cursor()
        _, _, filenames = next(walk('../out/'))
        for filename in filenames:
            f = open("../out/" + filename) 
            rows = csv.reader(f)
            next(rows, None) # skip the headers
            no_ext_name = path.splitext(filename)[0] 
            cur.execute("CREATE TABLE {} (timestamp, open, high, low, close, volume)".format(no_ext_name))
            cur.executemany("INSERT INTO {} VALUES (?, ?, ?, ?, ?, ?)".format(no_ext_name), rows)
        con.commit()
        con.close()
        logging.info("data successfully loaded")
    except Exception as e:
        logging.error(e)

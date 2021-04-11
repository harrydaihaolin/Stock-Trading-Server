import constants
import request_handler
import sys
import argparse
from datetime import datetime

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

def date_parser(date):
    try:
        date = datetime.fromisoformat(date)    
        return date;
    except ValueError as e:
        print(e)

try:
    parser.add_argument("-p", "--price", help=constants.PRICEHELP)
    parser.add_argument("-s", "--signal", help=constants.SIGNALHELP)
    parser.add_argument("-sa", "--server_address", help=constants.SERVERADDRESSHELP)
    parser.add_argument("-dt", "--del_ticker", help=constants.DELTICKERHELP)
    parser.add_argument("-at", "--add_ticker", help=constants.ADDTICKERHELP)
    parser.add_argument("-r", "--reset", action='store_true', help=constants.RESETHELP)
except:
    print("exception occured, exit program.")




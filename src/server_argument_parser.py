import logging
logging = logging.getLogger()
import constants
import request_handler
import sys
import argparse
# Parser of arguments
parser = argparse.ArgumentParser()

try:
    parser.add_argument("-i", "--interactive", action='store_true', help=constants.INTERACTIVEHELP)
    parser.add_argument("-t", "--tickers", nargs='*',help=constants.TICKERHELP)
    parser.add_argument("-p", "--port", help=constants.PORTHELP, type=int)
    parser.add_argument("-r", "--reload", help=constants.RELOADHELP)
    parser.add_argument("-m", "--minutes", help=constants.MINUTESHELP, required=('-t' in sys.argv or '--tickers' in sys.argv))
except:
    print("exception occured, exit program.")



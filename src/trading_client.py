import logging
logging.basicConfig(level=logging.INFO)
from client_argument_parser import parser 
import requests
import constants
import json
import re
from datetime import datetime

IPADDRESS = constants.IPADDRESS
PORT = constants.PORT
formatter="%Y-%m-%d-%H:%M"
def get_url(address, port):
    return "http://" + address + ":" + port 
URL=get_url(IPADDRESS, PORT)

def address_input_validator(address):
    return re.search("^\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}:\d{1,5}$", address)

def date_input_validator(date):
    try:
        datetime.strptime(date, formatter)
        logging.info("date format is correct")
        return True
    except ValueError as e:
        logging.error(e)

def get_price(date):
    try:
        if (date == 'now'):
            r = requests.get(URL+'/price/'+date)
        else:
            epoch = datetime.strptime(date, formatter).timestamp()
            r = requests.get(URL+'/price/' + str(int(epoch)))
        # it converts to dictionary string
        dictionary = json.loads(r.text)
        # it converts dictionary string to dictionary
        dictionary = json.loads(dictionary)
        return dictionary
    except Exception as e:
        print(e)

if __name__ == '__main__':
    args = parser.parse_args()
    if args.price and (args.price == 'now' or date_input_validator(args.price)):
        output = get_price(args.price)
        for k, v in output.items():
            if len(v) != 0: 
                print(k, v[0][0]) 
            else: 
                print(k, "No Data")
    elif args.price == 'now':
        # some code here
        pass

    if args.signal:
        print(args.signal)
    if args.server_address and address_input_validator(args.server_address):
        inp = args.server_address.split(':')
        URL=get_url(inp[0], inp[1])
        logging.info("Server address successfully setup")
    if args.del_ticker:
        print(args.del_ticker)
    if args.add_ticker:
        print(args.add_ticker)
    if args.reset:
        print(args.reset)
    # actions on argument 



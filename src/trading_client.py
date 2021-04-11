from client_argument_parser import parser, date_parser 
import http

client = http.client.HTTPConnection('localhost:8000')
client.send

if __name__ == '__main__':
    args = parser.parse_args()
    if args.price:
        date = date_parser(args.price)
        if date: print(date)
    if args.signal:
        print(args.signal)
    if args.server_address:
        print(args.server_address)
    if args.del_ticker:
        print(args.del_ticker)
    if args.add_ticker:
        print(args.add_ticker)
    if args.reset:
        print(args.reset)
    # actions on argument 



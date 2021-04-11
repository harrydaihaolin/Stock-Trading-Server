PORT="8080"
IPADDRESS="127.0.0.1"
ALPHAADVANTAGEKEY="6C6ZLWQNT2LK5OJG"
FINNHUBKEY="c1nnuv237fkph7jrlb70"
DATABASENAME="trading_database.db"
TICKERHELP="If specified, download data for all the US tickers specified. If this option is not specified, the server will download data for ticker ex: ‘AAPL.’ (Max of 3 tickers)"
PORTHELP="It specifies the network port for the server. This argument is optional, and default port is 8000."
RELOADHELP="If specified, the server will load historical data from the reload file instead of querying from Source 1"
MINUTESHELP="It specifies the sample data being downloaded. It only accepts (5,15,30,60) as inputs, and default value is 5."
INTERACTIVEHELP="It activates the interactive mode which is used for testing"
WELCOME="Welcome to the ALPHA Vantage trading interface, please type 'help' to get instructions"
PRICEHELP="""If specified, queries server for latest price
available as of the time specified. The time
queried is expected to be in UTC Time.
E.g. (Stock prices shown is not correct)
> client --price 2016-07-29-13:34
AAPL  	332.50
MSFT	180.30
FB	No Data
> client –-price 1959-05-14-01:00 
Server has no data 
> client --price 2025-05-14-01:00 
Server has no data
> client --price now
(latest stock price)
"""
SIGNALHELP="""If specified, queries server for latest trading 
signal available as of the time specified. The 
time queried is expected to be in UTC Time.
> client --signal 2016-07-28-15:43
(the answer here could be either 1, -1,0)
AAPL	1
MSFT	1
FB	0
> client –-signal 1995-05-14-01:00 
Server has no data 
> client –-signal 2025-05-14-01:00 
Server has no data
> client –-signal now
(latest signal value)
"""
SERVERADDRESSHELP="""If specified, connect to server running on the IP
address, and use specified port number. If this 
option is not specified, client assumes that the
server is running on 127.0.0.1:8000
"""
DELTICKERHELP="""Instruct the server to del a ticker from the server
database.

Returns 0=success, 1=server error, 2=ticker not found
"""
ADDTICKERHELP="""Instruct the server to add a new ticker to the server
database. Server must download historical data for said
ticker, and start appending on the next pull.

Returns 0=success, 1=server error, 2=invalid ticker
"""
RESETHELP="""
If specified, instructs the server to reset all the data.
Server must re-download data and tell client that it was
successful.

Client exits with return code: 0=success, 1=failure
"""

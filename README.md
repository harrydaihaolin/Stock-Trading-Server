# Trading Server Developer Instructions

## Install Dependencies 
```sh
pip3 install -r requirements.txt
```
## Help Text
```sh
python3 src/trading_server.py -h
python3 src/trading_client.py -h
```

## Deploy in Linux/Mac environment
- get the help text
```sh
python3 src/trading_server.py
```

## Deploy in Windows environment 
- wip

## Deploy in Docker environment
- wip

## Run the interactive console
```sh
python3 src/trading_server.py -i  
```

## Load the data with ticker and interval then start the server
- example:
```sh
python3 src/trading_server.py -t MSFT AAPL NIO -m 5 -p 8080
```
or
```sh
python3 src/trading_server.py --tickers MSFT AAPL NIO --minutes 5 --port 8080
```

## Meanwhile you should be able to see
```sh
out/$TICKER_result.csv that shows the trading strategy
out/$TICKER_price.csv that shows the timestamp and price
out/$TICKER.csv that shows the data pulled from Alpha Vantage
```

## start the client
- you can only specify the server address while you are running the command. (which means it's not stored inthe environment)
```sh
python3 src/trading_client.py --server_address 127.0.0.1:8080
```

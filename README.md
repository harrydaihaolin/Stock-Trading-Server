# Trading Server Developer Instructions

## File Structure Diagram
![file structure](https://user-images.githubusercontent.com/13538182/114333193-c06e3a80-9b15-11eb-8b7b-63344f63ec95.png)

## Install Dependencies 
```sh
pip3 install -r requirements.txt
```
## Help Text
```sh
python3 src/trading_server.py -h
python3 src/trading_client.py -h
```

## Deploy in Windows environment 
- In Windows, please install waitress, platform specific support is still work in progress

## Deploy in Docker environment
-  

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

## Comments on trading strategy
This trading strategy is a trend following strategy. Gathering the historical data can be misleading since we don't know if the market is going to jump or just turn back. Especially at the start of a new trend. Instead, in the long run, the profit would be relatively more stable than Mean Reversion strategies since the trend would be clearer as time goes by.

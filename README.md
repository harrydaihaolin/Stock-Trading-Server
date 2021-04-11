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

## Deploy in Docker environment

## Run the interactive console
```sh
python3 src/trading_server.py -i  
```

## Load the data and start the server
- example:
```sh
python3 src/trading_server.py -t MSFT AAPL NIO -m 5 -p 8080
```
or
```sh
python3 src/trading_server.py --tickers MSFT AAPL NIO --minutes 5 --port 8080
```

## start the client

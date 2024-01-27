# Fxopenpy

fxopenpy is a Python library for dealing with executing trading using Fxopen API.

## Installation

```Clone
git clone git@github.com:KrishnaInvestment/fxopenpy.git
cd algoapi
pip3 install . 
```
Alternatively you can install the package using PIP
```
pip install algoapi

```

## Usage

# Login
```python
from trades.open_position import Position

#to avoid entering the information each time maintain .env with variables
WEB_API_ID="WEB_API_ID"
WEB_API_KEY="WEB_API_KEY"
WEB_API_SECRET="WEB_API_SECRET"
API_URL="API_URL"

```

# Executing a trade
```python
#You can place market, limit, stop and stop_limit position
from trades.open_position import Position

position = Position('GBPUSD', 1000, 'Buy')

#Open market position
result_data = position.open_market_position()

#Add Stop Loss and Target
payload = {
    "stop_loss":1.4, # In Percentage
    "target":1.5, # In Percentage
    }

result_data = position.open_market_position(**payload)

#Add Expiry
payload = {
    "stop_loss":1.4, # In Percentage
    "target":1.5, # In Percentage
    "expiry":1,  # In Minutes
    }
result_data = position.open_market_position(**payload)

# Add Trigger
payload = {
    "contingent_order": True,
    "trigger_type": "OnTime",
    "trigger_time": 1,
    }

result_data = position.open_market_position(**payload)

#For more inputs please check 
#https://demo.forex.game/webapi?type=margin

# Add Limit Price
position = Position('GBPUSD', 1000, 'Buy')

data_input = {
    "price":price,
    }

result_data = position.open_market_position(**payload)

# Add Limit Price
position = Position('GBPUSD', 1000, 'Buy')

data_input = {
    "price":price,
    }

result_data = position.open_limit_position(**payload)

# Add Stop Limit Price
position = Position('GBPUSD', 1000, 'Buy')

data_input = {
    "stop_price": price
    }

result_data = position.open_stop_position(**payload)

# Add Stop Limit Price
position = Position('GBPUSD', 1000, 'Buy')

data_input = {
    "price":price,
    "stop_price": stop_price,
    }

result_data = position.open_stop_limit_position(**payload)


```
# Trades
```python
#Get trades list 
from trades.fetch_trades import FetchTrade


#Get Trades by Symbol
trades = FetchTrade().fetch_by_symbol('GBPUSD')

#Get Trade by ID
trades = FetchTrade().fetch_by_id('GBPUSD')

#Get All Trades
trades = FetchTrade().fetch_all('GBPUSD')

#If you are using then get Position using 
from trades.fetch_trades import FetchPosition

#Get Trades by Symbol
trades = FetchPosition().fetch_by_symbol('GBPUSD')

#Get Trade by ID
trades = FetchPosition().fetch_by_id('GBPUSD')

#Get All Trades
trades = FetchPosition().fetch_all('GBPUSD')
```


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.


## License

[MIT](https://choosealicense.com/licenses/mit/)
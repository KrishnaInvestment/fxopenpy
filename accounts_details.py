import requests
from fxopenheaders import get_auth_headers
import api_urls as apiurl
import json
import datetime
import requests
import pandas as pd


def get_account_info(key=None):
    url = apiurl.ACCOUNT_HISTORY

    response = requests.get(url, headers=get_auth_headers(url))

    response_text = json.loads(response.text)

    if key:
        return response_text.get(key)
    else:
        return response_text


def get_historical_currency_data(
    symbol, periodicity, last_n_days, no_of_bars, data_type
):
    custom_datetime = datetime.datetime.now() - datetime.timedelta(days=last_n_days)
    epoch_time_milliseconds = int(custom_datetime.timestamp() * 1000)

    url = (
        apiurl.QUOTEHISTORY_DATA % (symbol, periodicity, data_type)
        + f"?timestamp={epoch_time_milliseconds}&count={no_of_bars}"
    )
    response = requests.get(url, headers=get_auth_headers(url))

    response_text = json.loads(response.text)

    # data = get_historical_currency_data('EURUSD', 'M5', 5, 1000, 'ask')
    df = pd.DataFrame(response_text.get("Bars"))
    return df


def get_trades(id=None):
    url = apiurl.GET_ALL_TRADE

    if id:
        url = url + f"/{id}"

    response = requests.get(url, headers=get_auth_headers(url))

    # print(response.text)
    response_text = json.loads(response.text)

    if id:
        return pd.DataFrame.from_dict(response_text)

    df = pd.DataFrame(response_text)
    return df

def get_position(id=None):
    url = apiurl.GET_ALL_POSITION

    if id:
        url = url + f"/{id}"

    response = requests.get(url, headers=get_auth_headers(url))

    # print(response.text)
    response_text = json.loads(response.text)

    if id:
        return pd.DataFrame.from_dict(response_text)

    df = pd.DataFrame(response_text)
    return df

def close_trades(id, trade_type="Close"):
    url = apiurl.GET_ALL_TRADE + f"?trade.type={trade_type}&trade.id={id}"
    # print(get_auth_headers(url))
    response = requests.delete(url, headers=get_auth_headers(url, 'DELETE'))
    print(response.json())
    return response.text


def open_position(symbol, side, trade_type, amount):
    url = apiurl.GET_ALL_TRADE

    payload = {
        "Type": "Market",
        "Side": "Buy",
        "Symbol": "EURUSD",
        "Amount": 1000,
        "Comment": "Buy limit from Web API sample"
    }
    

    headers = get_auth_headers(url, "POST", payload)
    # 'yes'
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    print(response.json())

    # return response_text


trades = get_position()
print(trades)
for ids in trades.Id:
  close_trades(ids)

# dd = close_trades(175162425)
# print(dd)

# open_position('EURUSD', 'Buy', 'Market', 1000)

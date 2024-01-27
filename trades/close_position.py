import requests
from utils.fxopenheaders import get_auth_headers
import trades.urls as trade_url
from trades.constant import TRADE_DATA
import pandas as pd


def close_trades(id, trade_type="Close"):
    url = trade_url.GET_TRADE + f"?trade.type={trade_type}&trade.id={id}"
    response = requests.delete(url, headers=get_auth_headers(url, "DELETE"))
    print(response.json())
    return response.text

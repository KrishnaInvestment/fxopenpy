import trades.urls as trade_url
import pandas as pd
from utils.utils import RequstAPI


class TradePosition(RequstAPI):
    def __init__(self):
        self.URL = None

    def fetch_all(self):
        url = self.URL
        response_text = self.request_api(url)
        df = pd.DataFrame(response_text)
        return df

    def fetch_by_id(self, id):
        url = self.URL + f"/{id}"
        response_text = self.request_api(url)
        return pd.DataFrame.from_dict(response_text)

    def fetch_by_symbol(self, symbol):
        df = self.fetch_all()
        df = df[df["Symbol"] == symbol]
        return df


class FetchTrade(TradePosition):
    def __init__(self):
        self.URL = trade_url.GET_TRADE


class FetchPosition(TradePosition):
    def __init__(self):
        self.URL = trade_url.GET_POSITION

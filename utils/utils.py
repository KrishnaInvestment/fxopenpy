import requests
import json
import pandas as pd

import utils.base_urls as base_url
from utils.fxopenheaders import get_auth_headers
from utils.exceptions import APIError


class RequstAPI:
    def request_api(self, url, request_type="get", payload={}):
        if request_type == "get":
            response = requests.get(url, headers=get_auth_headers(url))
        elif request_type == "post":
            response = requests.post(
                url,
                data=json.dumps(payload),
                headers=get_auth_headers(url, "POST", payload),
            )
        elif request_type == "delete":
            response = requests.delete(url, headers=get_auth_headers(url))
        elif request_type == "put":
            response = requests.put(
                url,
                data=json.dumps(payload),
                headers=get_auth_headers(url, "PUT", payload),
            )
        try:
            response_text = json.loads(response.text)
        except Exception as e:
            raise APIError(str(e))
        else:
            if response.status_code in [200, 201]:
                return response_text
            else:
                raise APIError(response_text.get("Message"))


class Price(RequstAPI):
    def get_all_bid_price(self):
        url = base_url.GET_ALL_PRICE
        response_text = super().request_api(url)
        df = pd.DataFrame(response_text)
        response_text = response_text[0]
        return response_text.get("BestBid").get("Price")
    
    def get_latest_bid_price(self, symbol):
        url = base_url.GET_LATEST_PRICE % symbol
        response_text = super().request_api(url)
        response_text = response_text[0]
        return response_text.get("BestBid").get("Price")

    def get_latest_ask_price(self, symbol):
        url = base_url.GET_LATEST_PRICE % symbol
        response_text = super().request_api(url)
        response_text = response_text[0]
        return response_text.get("BestAsk").get("Price")

    @staticmethod
    def get_price(symbol, side):
        if side == "Buy":
            return Price().get_latest_ask_price(symbol)

        elif side == "Sell":
            return Price().get_latest_bid_price(symbol)


class Currency(RequstAPI):
    def __init__(self, columns=None):
        if columns:
            self.columns = columns
        else:
            self.columns = [
                "Name",
                "Type",
                "Tax",
                "Precision",
                "ExposureSwapSize",
                "DefaultStockFee",
                "Description",
            ]

    def all(self):
        currency = self.request_api(base_url.CURRENCY)
        df = pd.DataFrame(currency)
        return df[self.columns]

    def all_type(self):
        currency_type = self.request_api(base_url.CURRENCYTYPE)
        df = pd.DataFrame(currency_type)
        return df

    def filter_by_type(self, symbol_type):
        df = self.all()
        return df[df["Type"] == symbol_type]

    def filter_by_symbol(self, symbol):
        df = self.all()
        return df[df["Name"] == symbol]


class Symbol(RequstAPI):
    def __init__(self, columns=None):
        self.columns = columns

    def all(self):
        symbol = self.request_api(base_url.SYMBOL)
        df = pd.DataFrame(symbol)
        
        if self.columns:
            df = df[self.columns]  
        return df

    def all_type(self):
        symbol = self.request_api(base_url.SYMBOL)
        df = pd.DataFrame(symbol)
        return list(df.StatusGroupId.unique())

    def filter_by_type(self, symbol_type):
        df = self.all()
        return df[df["StatusGroupId"] == symbol_type]

    def filter_by_symbol(self, symbol):
        url = base_url.SYMBOL + f'/{symbol}'
        symbol = self.request_api(url)
        df = pd.DataFrame.from_dict(symbol)
        return df
    
    def get_columns(self):
        df = self.all()
        return list(df.columns)


    def get_all_pipsize(self, currency='USD'):
        url = base_url.PIPSIZE + f'?targetCurrency={currency}'
        pipsize = self.request_api(url)
        df = pd.DataFrame(pipsize)
        return df[['Symbol', 'Value']]
    
    def get_pipsize_by_symbol(self, symbol, currency='USD'):
        url = base_url.PIPSIZE + f'?targetCurrency={currency}&symbols={symbol}'
        pipsize = self.request_api(url)
        df = pd.DataFrame.from_dict(pipsize)
        return df[['Symbol', 'Value']]
    
    
    
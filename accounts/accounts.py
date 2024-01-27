import requests
from utils.fxopenheaders import get_auth_headers
import accounts.urls as account_url
from trades.constant import TRADE_DATA
import json
import pandas as pd


class AccountInfo:
    def get_account_information(self):
        url = account_url.ACCOUNT_HISTORY
        response = requests.get(url, headers=get_auth_headers(url))
        response_text = json.loads(response.text)
        return response_text

    def get_account_type(self):
        account_details = self.get_account_information()
        return account_details.get("AccountingType")

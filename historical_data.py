import datetime
import requests
from fxopenheaders import get_auth_headers
import api_urls as apiurl
import json
import pandas as pd

def get_historical_currency_data(symbol, periodicity, last_n_days, no_of_bars, data_type):
    custom_datetime = datetime.datetime.now() - datetime.timedelta(days=last_n_days)
    epoch_time_milliseconds = int(custom_datetime.timestamp() * 1000)
    
    url = apiurl.QUOTEHISTORY_DATA % (symbol, periodicity, data_type) + f"?timestamp={epoch_time_milliseconds}&count={no_of_bars}"
    response = requests.get(url, headers=get_auth_headers(url))
    
    response_text = json.loads(response.text)
    return response_text

data = get_historical_currency_data('EURUSD', 'M5', 5, 1000, 'ask')
df = pd.DataFrame(data.get('Bars'))



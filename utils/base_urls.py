import os

from dotenv import load_dotenv

load_dotenv()

API_URL = os.environ.get('API_URL')

#Price
GET_LATEST_PRICE = API_URL + "/api/v2/tick/%s"
GET_ALL_PRICE = API_URL + "/api/v2/tick"

#Currency
CURRENCY = API_URL + "/api/v2/currency"
CURRENCYTYPE = API_URL + "/api/v2/currencytype"

#Symbol
SYMBOL = API_URL + "/api/v2/symbol"

#PipSize
PIPSIZE = API_URL + "/api/v2/pipsvalue"
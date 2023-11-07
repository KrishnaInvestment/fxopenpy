import os

API_URL = os.environ.get('API_URL')

TRADESERVERINFO = API_URL + "/api/v2/tradeserverinfo"
TRADESESSION = API_URL + "/api/v2/tradesession"

CURRENCY = API_URL + "/api/v2/currency"
CURRENCYTYPE = API_URL + "/api/v2/currencytype"

SYMBOL = API_URL + "/api/v2/symbol"

QUOTEHISTORY = API_URL + "/api/v2/quotehistory/%s/%s/bars/ask/info"

QUOTEHISTORY_DATA = API_URL + "/api/v2/quotehistory/cache/%s/%s/bars/%s"

ACCOUNT_HISTORY = API_URL + "/api/v2/account"

GET_ALL_TRADE = API_URL + "/api/v2/trade"

GET_ALL_POSITION = API_URL + "/api/v2/position"


# GET /api/v2/tradesession
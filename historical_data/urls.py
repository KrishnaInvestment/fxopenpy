import os

API_URL = os.environ.get("API_URL")

QUOTEHISTORY = API_URL + "/api/v2/quotehistory/%s/%s/bars/%s/info"

QUOTEHISTORY_DATA = API_URL + "/api/v2/quotehistory/cache/%s/%s/bars/%s"

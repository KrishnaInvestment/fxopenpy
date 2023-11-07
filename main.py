import requests
from fxopenheaders import get_auth_headers
import api_urls as apiurl
import json
# headers = get_auth_headers()
url = apiurl.QUOTEHISTORY % ('EURUSD', 'M5')
url = apiurl.TRADESESSION

print(url)
response = requests.get(url, headers=get_auth_headers(url))

response_text = json.loads(response.text)
print(response_text)
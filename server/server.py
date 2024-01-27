import requests
from utils.fxopenheaders import get_auth_headers
import server.urls as apiurl
import json


def get_tradeserver_info():
    url = apiurl.TRADESERVERINFO

    response = requests.get(url, headers=get_auth_headers(url))

    response_text = json.loads(response.text)

    return response_text


def get_tradesession_info():
    url = apiurl.TRADESESSION

    response = requests.get(url, headers=get_auth_headers(url))

    response_text = json.loads(response.text)

    return response_text

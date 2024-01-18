import os
import hashlib
import hmac
import base64
import json
import time
from dotenv import load_dotenv

load_dotenv()

web_api_id = os.environ.get('WEB_API_ID')
web_api_key = os.environ.get('WEB_API_KEY')
web_api_secret = os.environ.get('WEB_API_SECRET')

def calculate_hmac_with_sha256(signature):
    digest_value = hmac.new(web_api_secret.encode("utf-8"),
                            msg=signature.encode("utf-8"),
                            digestmod=hashlib.sha256).digest()
    hash_value = base64.b64encode(digest_value)
    return hash_value.decode("utf-8")

def get_auth_headers(api_url, http_method='GET', payload_data=None):
    headers = {
    'Accept-Encoding': 'gzip, deflate',
    'Content-type': 'application/json',
    }
    timestamp = str(int(time.time() * 1000)) 
    #This is timestamp in web portal
    # timestamp = str(1699110193129)
    payload_data = '' if payload_data is None else json.dumps(payload_data)
    signature = f'{timestamp}{web_api_id}{web_api_key}{http_method}{api_url}{payload_data}'
    hash_value = calculate_hmac_with_sha256(signature)
    auth_value = 'HMAC {0}:{1}:{2}:{3}'.format(web_api_id, web_api_key, timestamp, hash_value)
    headers['Authorization'] = auth_value
    return headers
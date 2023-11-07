import os
import hashlib
import hmac
import base64
import json
import time

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


# def get_auth_headers(api_url, http_method='GET', payload_data=None):

#     # Generate a unique timestamp in milliseconds
#     timestamp_ms = str(int(time.time() * 1000))

#     # Create the signature
#     signature = f"{timestamp_ms}{web_api_id}{web_api_key}{http_method}{api_url}"
#     if payload_data:
#         signature += json.dumps(payload_data)
        
#     signature = signature.encode('utf-8')
#     hmac_signature = hmac.new(web_api_secret.encode('utf-8'), signature, hashlib.sha256).digest()
#     base64_signature = base64.b64encode(hmac_signature).decode('utf-8')

#     # Construct the Authorization header
#     authorization_header = f'HMAC {web_api_id}:{web_api_key}:{timestamp_ms}:{base64_signature}'

#     # Set up the headers
#     headers = {
#         'Accept-Encoding': 'gzip, deflate',
#         'Content-type': 'application/json',
#         'Authorization': authorization_header
#     }

#     return headers
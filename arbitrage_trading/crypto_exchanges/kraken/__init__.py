import os
import time
import base64
import hashlib
import hmac
from urllib import request
import json
from dotenv import load_dotenv

load_dotenv()


def get_websocket_token():
    # Variables (API method, nonce, and POST data)
    api_nonce = str(int(time.time() * 1000))
    api_post = 'nonce=' + api_nonce

    # Cryptographic hash algorithms
    api_sha256 = hashlib.sha256(api_nonce.encode('utf-8') + api_post.encode('utf-8'))
    api_hmac = hmac.new(base64.b64decode(os.environ.get("KRAKEN_API_PRIVATE")),
                        os.environ.get("KRAKEN_API_PATH").encode('utf-8') + api_sha256.digest(), hashlib.sha512)

    # Encode signature into base64 format used in API-Sign value
    api_signature = base64.b64encode(api_hmac.digest())

    # HTTP request (POST)
    api_request = request.Request('https://api.kraken.com/0/private/GetWebSocketsToken', api_post.encode('utf-8'))
    api_request.add_header('API-Key', os.environ.get("KRAKEN_API_KEY"))
    api_request.add_header('API-Sign', api_signature)
    api_response = request.urlopen(api_request).read().decode()

    #print(os.environ.get("KRAKEN_API_KEY"), os.environ.get("KRAKEN_API_PRIVATE"))

    print(json.loads(api_response))
    token = json.loads(api_response)['result']['token']
    print(token)

    # Output API response
    return token

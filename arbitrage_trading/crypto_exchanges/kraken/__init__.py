import os
import time
import base64
import hashlib
import hmac
import urllib
from urllib import request
import json
from dotenv import load_dotenv
import requests

load_dotenv()

assets_method_mapping = {
    "USDT": "Tether USD (TRC20)",
    "ETH": "Ethereum (ERC20)",
    "BTC": "Bitcoin",
    "LTC": "Litecoin",
}


def get_api_signature(urlpath, data):
    postdata = urllib.parse.urlencode(data)
    encoded = (str(data['nonce']) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()

    mac = hmac.new(base64.b64decode(os.environ.get("KRAKEN_API_PRIVATE")), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    return sigdigest.decode()


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

    # print(os.environ.get("KRAKEN_API_KEY"), os.environ.get("KRAKEN_API_PRIVATE"))

    print(json.loads(api_response))
    token = json.loads(api_response)['result']['token']
    print(token)

    # Output API response
    return token


# Attaches auth headers and returns results of a POST request
def kraken_request(uri_path, data):
    headers = {
        'API-Key': os.environ.get("KRAKEN_API_KEY"),
        'API-Sign': get_api_signature(uri_path, data)
    }
    req = requests.post((os.environ.get("KRAKEN_API_URL") + uri_path), headers=headers, data=data)
    # print(headers)
    return req


def add_order(order):
    # Construct the request and print the result
    resp = kraken_request('/0/private/AddOrder', {
        "nonce": str(int(1000 * time.time())),
        "ordertype": "market",
        "type": "buy",
        "volume": 1.25,
        "pair": "XBTUSD",
        "price": 27500
    })
    print(resp.json())


def get_account_balance():
    # Construct the request and print the result
    resp = kraken_request('/0/private/Balance', {
        "nonce": str(int(1000 * time.time()))
    })
    print(resp.json())


def get_address(asset, method):
    def address(is_new=False):
        return kraken_request('/0/private/DepositAddresses', {
            "nonce": str(int(1000 * time.time())),
            "asset": asset,
            "method": method,
            "new": is_new
        }).json()

    res = address()
    if res["result"].__len__() == 0:
        res = address(True)

    print(res)


def get_deposit_method(asset):
    # Construct the request and print the result
    resp = kraken_request('/0/private/DepositMethods', {
        "nonce": str(int(1000 * time.time())),
        "asset": asset
    })
    print(resp.json())

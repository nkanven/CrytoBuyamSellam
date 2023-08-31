import os
from kucoin.client import User

try:
    client = User(
        os.environ.get("KUCOIN_API_KEY"),
        os.environ.get("KUCOIN_API_SECRET"),
        os.environ.get("KUCOIN_API_PASSPHRASE")
    )
except Exception as e:
    print(str(e))
import os, requests
from dotenv import load_dotenv

load_dotenv()


def notify(text):
    url = f"https://api.telegram.org/{os.environ.get('TELEGRAM_BOT_ID')}/sendMessage?chat_id={os.environ.get('TELEGRAM_CHAT_ID')}&text={text}"
    requests.get(url)

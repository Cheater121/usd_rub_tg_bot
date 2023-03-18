import logging
import requests
import datetime
from time import sleep
from tokens import tg_token, exch_token

class ExchangeBot:
    id = None
    last_rate = 75
    red_apple = "\U0001F34E"
    green_apple = "\U0001F34F"
    ice = "\U0001F9CA"
    up = "\U00002B06"
    down = "\U00002B07"
    flat = "\U00002195"

    def __init__(self, tg_token, exch_token):
        self.tg_token = tg_token
        self.exch_token = exch_token
        # Set up the logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.ERROR)
        # Create a file handler
        handler = logging.FileHandler('error.log')
        handler.setLevel(logging.ERROR)
        # Create a logging format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        # Add the handler to the logger
        self.logger.addHandler(handler)

    def get_exchange_rate(self):
        url = "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=1"
        headers = {"apikey": self.exch_token}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            result = response.json()
            exchange_rate = result.get("result")
            return exchange_rate
        except Exception as e:
            self.logger.exception(e)
            return None

    def make_text(self, exchange_rate):
        try:
            if exchange_rate is None:
            	text = "\U0001F198\U0001F198\U0001F198 \U0001F4B1\U00002620"
            	return text
            percent = (exchange_rate / self.last_rate - 1) * 100
            percent = round(percent, 2)
            if percent < 0:
                apple = self.red_apple
                direction = self.down
                symbol = ""
            elif percent == 0:
                apple = self.ice
                direction = self.flat
                symbol = ""
            else:
                apple = self.green_apple
                direction = self.up
                symbol = "+"
            self.last_rate = exchange_rate
            text = f"1$ = {round(exchange_rate,2)}₽, {symbol}{percent}% {apple}{direction}"
            return text
        except Exception as e:
            self.logger.exception(e)
            return None

    def send_message(self, chat_id, text):
        try:
            message = {"chat_id": chat_id, "text": text}
            method = "sendMessage"
            url = f"https://api.telegram.org/bot{self.tg_token}/"
            resp = requests.post(url + method, message)
            resp.raise_for_status()
            return resp.text
        except Exception as e:
            self.logger.exception(e)
            return None

    def get_chat_id(self):
        if self.id is None:
            method = "getUpdates"
            url = f"https://api.telegram.org/bot{self.tg_token}/"
            params = {"offset": -1}  # get only last message
            try:
                resp = requests.get(url + method, params)
                resp.raise_for_status()
                resp_array = resp.json().get("result")
                chat_id = resp_array[0]["message"]["chat"]["id"]
                self.id = chat_id
                return chat_id
            except Exception as e:
                self.logger.exception(e)
                return None
        else:
            return self.id


bot = ExchangeBot(tg_token, exch_token)
while True:
    now = datetime.datetime.now()
    start = datetime.time(10, 0, 0, 0)
    stop = datetime.time(20, 0, 0, 0)
    if start < now.time() < stop and now.weekday() not in (5, 6):
        print(now)
        chat_id = bot.get_chat_id()
        exchange_rate = bot.get_exchange_rate()
        text = bot.make_text(exchange_rate)
        bot.send_message(chat_id, text)
        sleep(60 * 60 * 3)
    print("weekend")
    sleep(60)
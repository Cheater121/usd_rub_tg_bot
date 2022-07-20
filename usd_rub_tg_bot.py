import requests
import datetime
from time import sleep
from tokens import tg_token, exch_token


class ExchangeBot:
    last_rate = 55
    red_apple = "\U0001F34E"
    green_apple = "\U0001F34F"
    up = "\U00002B06"
    down = "\U00002B07"

    def __init__(self, tg_token, exch_token):
        self.tg_token = tg_token
        self.exch_token = exch_token

    def get_exchange_rate(self):
        url = "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=1"
        headers = {"apikey": self.exch_token}
        response = requests.get(url, headers=headers)
        result = response.json()
        exchange_rate = result.get("result")
        return exchange_rate

    def make_text(self, exchange_rate):
        percent = (exchange_rate / self.last_rate - 1) * 100
        percent = round(percent, 4)
        if percent < 0:
            apple = self.red_apple
            direction = self.down
        else:
            apple = self.green_apple
            direction = self.up
        self.last_rate = exchange_rate
        text = f"Курс доллара к рублю составляет: {exchange_rate}. Относительно предыдущего значения курс изменился на {percent}% {apple}{direction}"
        return text

    def send_message(self, chat_id, text):
        message = {"chat_id": chat_id, "text": text}
        method = "sendMessage"
        url = f"https://api.telegram.org/bot{self.tg_token}/"
        resp = requests.post(url + method, message)
        return resp.text

    def get_chat_id(self):
        method = "getUpdates"
        url = f"https://api.telegram.org/bot{self.tg_token}/"
        params = {"offset": -1}  # get only last message
        resp = requests.get(url + method, params)
        resp_array = resp.json().get("result")
        chat_id = resp_array[0]["message"]["chat"]["id"]
        return chat_id


bot = ExchangeBot(tg_token, exch_token)
while True:
    now = datetime.datetime.now().time()
    start = datetime.time(10, 0, 0, 0)
    stop = datetime.time(20, 0, 0, 0)
    if start < now < stop:
        print(now)
        chat_id = bot.get_chat_id()
        exchange_rate = bot.get_exchange_rate()
        text = bot.make_text(exchange_rate)
        bot.send_message(chat_id, text)
        sleep(60 * 60 * 3)

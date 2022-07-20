import requests
import datetime
from time import sleep
from tokens import tg_token, exch_token

class ExchangeBot:
 	last_rate = 55
 	
 	def __init__(self, tg_token, exch_token):
 		self.tg_token = tg_token
 		self.exch_token = exch_token
 	
 	
 	def get_exchange_rate(self):
 		url = "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=1"
 		headers = {"apikey": self.exch_token}
 		response = requests.get(url, headers=headers)
 		result = response.json()
 		answer = result.get("result")
 		return answer
 	
 			
 	def send_message(self, chat_id):
 		text = self.get_exchange_rate()
 		red_apple = "\U0001F34E"
 		green_apple = "\U0001F34F"
 		percent = text/self.last_rate - 1
 		if percent < 0:
 			apple = red_apple
 		else:
 			apple = green_apple
 		percent = round(percent, 4)
 		message = {"chat_id": chat_id, "text": f"Курс доллара к рублю составляет: {text}. Относительно предыдущего значения курс изменился на {percent} % {apple}"}
 		method = "sendMessage"
 		url = f"https://api.telegram.org/bot{self.tg_token}/"
 		resp = requests.post(url + method, message)
 		return resp.text
 		
 		
 	def get_chat_id(self):
 		method = "getUpdates"
 		url = f"https://api.telegram.org/bot{self.tg_token}/"
 		params = {"offset": -1} # get only last message
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
		bot.send_message(bot.get_chat_id())
		sleep(60*60*3)
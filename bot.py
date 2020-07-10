import requests
import telebot
import os

# f = open('token.txt')
# TOKEN = f.readline()
TOKEN = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
	bot.send_message(message.chat.id, 'Привет, введи имя акции и получи ее стоимость.')

@bot.message_handler(content_types=['text'])
def text_handler(message):
	text = message.text.lower()
	chat_id = message.chat.id
	a = requests.get('https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities/' + text + '.json?iss.meta=off&iss.only=securities&securities.columns=SECID,PREVADMITTEDQUOTE')
	resp = a.json()['securities']['data']
	resp = resp[0]
	msg = resp[0] + ' : ' + str(resp[1]) 
	bot.send_message(chat_id, msg)

bot.polling()
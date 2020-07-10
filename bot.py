import requests
import telebot
import os

vowel = set("аеёиоуэюя")
consonant = set("цкнггшщзхждлрпвфчсмтб")

TOKEN = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
	chat_id = message.chat.id
	text = message.text
	msg = bot.send_message(chat_id, 'Привет, как тебя зовут?')
	bot.register_next_step_handler(msg, askAge)

def askAge(message):
	chat_id = message.chat.id
	text = message.text
	# if not text.isdigit():
	#     msg = bot.send_message(chat_id, 'Возраст должен быть числом, введите ещё раз.')
	#     bot.register_next_step_handler(msg, askAge) #askSource
	#     return
	ending = text.lower()[-3:]
	sign = ending[0]
	
	if sign == 'а':
		ending = 'я' + ending[-2:]
	if sign in consonant:
		ending = 'я' + ending
	
	huname = 'Ху' + ending
	msg = bot.send_message(chat_id, huname)


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
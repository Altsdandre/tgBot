import requests
import telebot
import os

vowel = set("аеёиоуэюяы")
consonant = set("цкнггшщзхждлрпвфчсмтбьъ")
alphabet=set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')

TOKEN = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
	chat_id = message.chat.id
	text = message.text
	msg = bot.send_message(chat_id, 'Привет, как твоё имя?')
	bot.register_next_step_handler(msg, askName)

def askName(message):
	chat_id = message.chat.id
	text = message.text
	responseName(text, chat_id)

def matchRu(text):
	return not alphabet.isdisjoint(text.lower())

def checkInput(text):
	if not text.isalpha():
		return 'notalpha'
	if matchRu(text):
		return 'ru'
	else:
		return 'en'

def responseName(name, chat_id):
	text = name.strip()
	if not checkInput(text) == 'ru':
		msg = bot.send_message(chat_id, 'Русиш онли')
		return

	text = text.lower()
	ending = text
	firstVowel = -1
	for i in range(0, len(text)):
		if text[i] in vowel:
			ending = text[i:]
			firstVowel = i
			break
	if ending == text and firstVowel == -1:
		msg = bot.send_message(chat_id, "Хуя" + ending)
		return

	if len(ending) > 1 and ending[1] in vowel:
		ending = ending[1:]

	if ending == "я":
		msg = bot.send_message(chat_id, "Головка от хуя!")
		return

	sign = ending[0]
	
	if len(text) < 2:
		msg = bot.send_message(chat_id, 'Съешь растишку')
		return
	elif len(text) == 2:
		if text[0] == 'у':
			ending = 'ю' + text[1]
		else:
			ending = text
	elif sign == 'а':
		ending = 'я' + ending[1:]
	elif sign == 'о':
		ending = 'ё' + ending[1:]
	elif sign == 'у':
		ending = 'ю' + ending[1:]
	elif sign in consonant:
		precons = text[-4:-3]
		signcons = text[-5:-4]
		if precons in consonant:
			ending = precons + ending
			if signcons == 'а':
				ending = 'я' + ending
			elif signcons == 'о':
				ending = 'ё' + ending
			elif signcons == 'у':
				ending = 'ю' + ending
			else:
				ending = signcons + ending
		else:
			if precons == 'а':
				ending = 'я' + ending
			elif precons == 'о':
				ending = 'ё' + ending
			elif precons == 'у':
				ending = 'ю' + ending
			else:
				ending =  precons + ending
	
	huname = 'Ху' + ending
	msg = bot.send_message(chat_id, huname)

def responseData(name, chat_id):
	text = name.strip()
	if not checkInput(text) == 'en':
		msg = bot.send_message(chat_id, 'wrong name')
		return
	a = requests.get('https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities/' + text + '.json?iss.meta=off&iss.only=securities&securities.columns=SECID,PREVADMITTEDQUOTE')
	resp = a.json()['securities']['data']
	if resp:
		resp = resp[0]
		msg = resp[0] + ' : ' + str(resp[1])
		bot.send_message(chat_id, msg)
	else:
		bot.send_message(chat_id, 'no data')

@bot.message_handler(commands=['zoo'])
def qest_handler(message):
	chat_id = message.chat.id
	text = message.text
	msg = bot.send_message(chat_id, 'Сколько будет 150+150?')
	bot.register_next_step_handler(msg, askNum)

def askNum(message):
	chat_id = message.chat.id
	text = message.text
	text = text.lower()
	
	if text.isdigit():
		if text == '300':
			bot.send_message(chat_id, 'Атсаси у трактариста!')
		else:
			bot.send_message(chat_id, 'Дурачина!')
	elif text == 'триста':
		bot.send_message(chat_id, 'Атсаси у трактариста!')
	else:
		bot.send_message(chat_id, 'Дурачина!')

@bot.message_handler(content_types=['text'])
def text_handler(message):
	text = message.text.lower()
	chat_id = message.chat.id

	if text.isdigit():
		if text == '300':
			bot.send_message(chat_id, 'Атсаси у трактариста!')
		else:
			bot.send_message(chat_id, 'Это не твое любимое число')	
	elif checkInput(text) == 'en':
		responseData(text, chat_id)
	else:
		responseName(text, chat_id)

bot.polling()
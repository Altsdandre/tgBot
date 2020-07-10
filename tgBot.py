import requests
import json

f = open('token.txt')
token = f.readline()

name = 'AFKS'

a = requests.get('https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities/' + name + '.json?iss.meta=off&iss.only=securities&securities.columns=SECID,PREVADMITTEDQUOTE')

resp = a.json()['securities']['data']
resp = resp[0]
message = resp[0] + ' : ' + str(resp[1]) 
#print(message)

url = 'https://api.telegram.org/bot'+ token +'/sendMessage?chat_id=-430753446'
data={'text':message}

tgmess=requests.post(url, json=data)
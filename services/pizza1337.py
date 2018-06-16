from lxml import html
import requests
from pwn import *
from random import randint
import sys

def get_flag(host, port, flag_id, token):
	
	username = flag_id.split(" ")[0]
	password = flag_id.split(" ")[1]
	
	trackinfo = {"orderid" : username, "password" : password, "token" : token}
	session = requests.Session()
	
	response = session.post('http://'+host+':20140/1337_pizza.cgi/tracking.html', data= trackinfo)
	
	flags=re.search(r'Payment processed via (.*?)$', response.content)


	if flags:
		oldFlag = flags.group(1)
		return oldFlag[3:]

def set_flag(host, port, flag):
	firstname = genRndString()
	lastname = genRndString()
	password = genRndString()
	reginfo = {"username" : firstname + " " + lastname,
	         "password" : password}
	
	session = requests.Session()
	
	response = session.post('http://'+host+':20140/1337_pizza.cgi/register.html', data = reginfo)

	numbers=re.findall(r'\d+', response.content)
	if len(numbers) == 1:
		customerid=numbers[0]
		response = session.post('http://'+host+':20140/1337_pizza.cgi/order.html', data={"customerid": customerid, "payment_information": "FLG"+flag, "address_line_1": genRndString(), "password": password, "address_line_2": genRndString()+" "+genRndString(), "items": "Hawaii"})
		successPtr = response.content.find( "OrderNr" )
		if successPtr != -1:
			numbers= re.findall(r'\d+', response.content)
			tokens = re.findall(r'\bToken: \w+', response.content)
			cookie = numbers[0] + ";" + password + ";" + tokens[0][7:]
			#print "COOKIE:",cookie
	
	dati = cookie.split(";")
	
	flag_id = dati[0] + " " + dati[1]
	
	token = dati[2]
	
	return {"flag_id": flag_id, "token": token}
	
def genRndString():
        rang = randint(8,16)
        rndString = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(rang))
        return rndString


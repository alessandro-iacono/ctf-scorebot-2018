from lxml import html
import requests
from pwn import *
from random import randint
import sys

def get_flag(host, port, flag_id, token):
	infos = {"username" : flag_id, "password" : token}
	login = requests.post('http://'+host+':20136/fuckapache.cgi/login', data = infos)
	
	
	session = requests.Session()
		
	target_tree = html.fromstring(login.content)
	
	flag = (target_tree.xpath('//*[@class="draft top"]/textarea'))[0]
	
	return flag.text
	

def set_flag(host, port, flag):
	username = genRndString()
	password = genRndString()
	infos = {"username" : username, "password" : password}
	register = requests.post('http://'+host+':20136/fuckapache.cgi/register', data = infos)
	
	session = requests.Session()
	
	login = session.post('http://'+host+':20136/fuckapache.cgi/login', data = infos)
	
	payload = {
	"data" : flag,
	"action" : "new"
	}
		
	submit = session.post('http://'+host+':20136/fuckapache.cgi/draft', data = payload)
				
	return {"flag_id": username, "token": password}
	
def genRndString():
        rang = randint(8,16)
        rndString = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(rang))
        return rndString

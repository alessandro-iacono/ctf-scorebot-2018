from lxml import html
import requests
from pwn import *
from random import randint
import sys
import re

def get_flag(host, port, flag_id, token):
	infos = {"login" : flag_id,
             "password" : token,
             "action" : "signin"}
	
	session = requests.Session()

	
	login = session.post('http://'+host+':20120/', data = infos)	
	
	target = re.findall(r'<p class="content">(.*?)</p>', login.text)
	
	
	return target[len(target) - 1]
	

def set_flag(host, port, flag):
	username = genRndString()
	password = genRndString()
	infos = {"name" : username,
	         "login" : username,
             "password" : password,
             "action" : "signup"}
	session = requests.Session()
	
	register = session.post('http://'+host+':20120/', data = infos)
		
	payload = {
	"content" : flag,
	"action" : "addsecret"
	}
		
	submit = session.post('http://'+host+':20120/', data = payload)
	
	payload = {
	"action" : "logout"
	}
	
	submit = session.post('http://'+host+':20120/', data = payload)
			
	return {"flag_id": username, "token": password}
	
def genRndString():
        rang = randint(8,16)
        rndString = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(rang))
        return rndString

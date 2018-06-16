import time, threading
import random, string
from pwn import *
from random import randint
import sys

context.log_level = 'error'

def get_flag(host, port, flag_id, token):
	c = remote(host,port)

	for i in range(7):
		c.recvline()
	
	c.sendline("1")

	for i in range(7):
		c.recvline()
	
	c.sendline("Y")
	c.recvline()
	c.recvline()
	c.sendline(str(token)+str(flag_id))

	data = c.recvline()
	data = data[16:-1]
	c.close()
	return data

def set_flag(host, port, flag):
	flag_id = genFlagID()
	password = genPasswd()
	c = remote(host,port)
	for i in range(7):
		c.recvline()
	
	c.sendline("2")
	for i in range(6):
		c.recvline()
	
	c.sendline(str(password)+str(flag_id))
	c.sendline(flag)
	c.recvline()
	c.recvline()
	c.close()
	return {"flag_id": flag_id, "token": password}
	#return flag_id, password 
	
def genFlagID():
	flag_id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))
	return flag_id
	
def genPasswd():
	password = randint(0,9999)
	return password
	
#flag_id, token = set_flag("10.7.40.2","20109","Ciao")

#print get_flag("10.7.40.2","20109",flag_id,token)


from pwn import *
from random import randint
import sys

context.log_level = 'error'

def get_flag(host, port, flag_id, token):
	c = remote(host,port)
	
	for i in range(6):
		c.recvline()
	c.sendline(str(flag_id))
	c.sendline(str(token))
	c.sendline()
	
	for i in range(6):
		c.recvline()
		
	c.sendline("R")	
	data = c.recvline()
	data = data[:-1]
	c.close()
	return data

def set_flag(host, port, flag):
	flag_id = genFlagID()
	password = genPasswd()
	c = remote(host,port)
	for i in range(6):
		c.recvline()
	c.sendline(str(flag_id))
	c.sendline(str(password))
	c.sendline(str(flag))
	
	for i in range(6):
		c.recvline()
		
	c.sendline("S")	
	c.recvline()
	c.sendline("V0=V2+4\n")
	c.recvline()
	
	c.close()
	return {"flag_id": flag_id, "token": password}

def genFlagID():
	flag_id = randint(0,999999999)
	return flag_id
	
def genPasswd():
	password = randint(100,10000)
	return password
	
#set_flag("10.7.40.2","20046","Lorenzo")
#print get_flag("10.7.40.2","20046",flag_id,token)


from pwn import *
from random import randint
import sys

context.log_level = 'error'

def get_flag(host, port, flag_id, token):
	c = remote(host,port)
	for i in range(12):
		c.recvline()
	c.sendline("1")
	c.sendline(str(flag_id))
	c.recvline()
	c.sendline(str(token))
	for i in range(11):
		c.recvline()
	c.sendline("6")	
	c.recvline()
	data = c.recvline()
	data = data[:-1]
	c.close()
	return data

def set_flag(host, port, flag):
	flag_id = genFlagID()
	password = genPasswd()
	c = remote(host,port)
	for i in range(12):
		c.recvline()
	c.sendline("2")
	c.sendline(str(flag_id))
	c.recvline()
	c.sendline(str(password))
	c.recvline()
	c.recvline()
	c.recvline()
	c.recvline()
	c.sendline("y\n")
	for i in range(19):
		c.recvline()
	
	c.sendline("1")
	c.sendline(str(flag_id))
	c.recvline()
	c.sendline(str(password))
	
	for i in range(10):
		c.recvline()
	
	c.sendline("3")	
	c.recvline()
	c.recvline()
	c.recvline()
	c.sendline("20")
	c.recvline()
	c.sendline(str(flag))

	c.recvline()

	c.close()
	return {"flag_id": flag_id, "token": password}
	
def genFlagID():
	flag_id = randint(0,999999999)
	return flag_id
	
def genPasswd():
	password = randint(100,10000)
	return password

#set_flag("10.7.40.2",20126,"CIAOCIAO")
#print get_flag("10.7.40.2",20126,"797467826","7713")


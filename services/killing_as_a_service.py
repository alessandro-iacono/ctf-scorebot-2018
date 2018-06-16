from pwn import *
from random import randint
import sys

context.log_level = 'error'

def get_flag(host, port, flag_id, token):
	c = remote(host,port)
	for i in range(18):
		c.recvline()
	c.sendline("1")
	
	for i in range(34):
		c.recvline()
	
	c.sendline("1")
	
	for i in range(10):
		c.recvline()
	
	c.sendline(flag_id)
	
	c.sendline()

	for i in range(10):
		c.recvline()
		
	c.sendline("1")
	
	c.sendline(token)

	
	for i in range(15):
		c.recvline()
	data = c.recvline()
	data = data[11:-1]
	data
	c.close()
	return data

def set_flag(host, port, flag):
	c = remote(host,port)
	for i in range(18):
		c.recvline()
	c.sendline("2")
	for i in range(35):
		c.recvline()
	c.sendline("1")
	c.sendline("trace")
	c.sendline(str(flag))
	c.sendline()
	
	for i in range(14):
		c.recvline()
		
	flag_id = c.recvline()
	flag_id = flag_id[13:-1]
	password = c.recvline()
	password = password[17:-1]
	
	c.close()
	return {"flag_id": flag_id, "token": password}
	

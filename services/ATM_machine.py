from pwn import *
from random import randint
import sys

def get_flag(host, port, flag_id, token):
	#print("flag Get: " + flag_id + token)        
	c = remote(host,port)
	for count in range(0,7):
        	c.recvline()	        
	c.sendline("1")
        c.recvline()
        c.recvline()
	c.sendline(flag_id)
	c.recvline()
	c.sendline(token)
	c.recvline()
	data = token[:20]
	c.close()
	return data
        
def set_flag(host, port, flag):
        flag_id = genFlagID()
        password = genRndString(flag)
        c = remote(host,port)
        for count in range(0,7):
        	c.recvline()	        
	c.sendline("3")
        c.recvline()
        c.recvline()
	c.recvline()
	c.sendline(flag_id)
        c.recvline()
	c.sendline(password)
        c.close()
        return {"flag_id": flag_id, "token": password}

def genRndString(flag):
        rang = randint(8,16)
        rndString = flag+''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(rang))
        return rndString 

def genFlagID():
        flag_id = randint(0,999999999)
        return str(flag_id)

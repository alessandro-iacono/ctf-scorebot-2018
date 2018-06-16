from pwn import *
from random import randint
import sys

def get_flag(host, port, flag_id, token):
        c = remote(host,port)
        c.recvline() 
        c.recvline() 
        c.recvline() 
        c.recvline() 
        c.recvline() 
        c.recvline() 
        c.recvline() 
        c.recvline()
        c.sendline("7")
        c.recvline()
        c.sendline(str(flag_id) + " " + str(token) + "\n")
        data = c.recvline()
        data = data[17:].strip()
        c.close()
        return data

def set_flag(host, port, flag):
        flag_id = genFlagID()
        password = genPasswd()
        c = remote(host, port)
        c.recvline()
        c.recvline() 
        c.recvline() 
        c.recvline() 
        c.recvline() 
        c.recvline() 
        c.recvline() 
        data = c.recvline()
        c.sendline("6") 
        c.recvline() 
        c.recvline()
        c.sendline(str(flag_id) + " " + str(password) + " " + str(flag) + "\n")
         
        c.recvline() 
        c.recvline() 
        c.recvline() 
        c.recvline() 
        c.recvline() 
        c.recvline() 
        c.recvline() 
        c.recvline()
        c.sendline("5")
        c.close()
        return {"flag_id": flag_id, "token":password} 

def genFlagID():
    flag_id = randint(0,999999999)
    return flag_id

def genPasswd():
        rang = randint(8,16)
        password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(rang))
        return password

from pwn import *
from random import randint
import sys

def get_flag(host, port, flag_id, token):
        
        c = remote(host,port)
        for count in range(0,5):
                c.recvline()
        
        # Login
        c.sendline("L")
        c.recvline()
        c.recvline()
        c.sendline(token.split()[0])
        c.recvline()
        c.sendline(token.split()[1])

        for count in range(0,4):
                c.recvline()

        # Decode message
        c.sendline("G")      
        c.recvline()
        c.sendline(flag_id.split()[0])
        c.sendline(flag_id.split()[1])
        c.recvline()
        data = c.recvline()
        c.close()
        return data.replace('\n','')

def set_flag(host, port, flag):
        #print("flag set: " + flag)
        
        password = genRndString()
        username = genRndString()
        
        c = remote(host,port)
        for count in range(0,5):
                c.recvline()
        
        # Register
        c.sendline("R")
        c.recvline()
        c.recvline()
        c.sendline(username)
        c.recvline()
        c.sendline(password)
        
        for count in range(0,5):
                c.recvline()
        
        # Login
        c.sendline("L")
        c.recvline()
        c.recvline()
        c.sendline(username)
        c.recvline()
        c.sendline(password)       
        
        for count in range(0,4):
                c.recvline()

        c.sendline("C")
        c.recvline()
        c.sendline(flag)

        c.recvline()
        token = c.recvline()
        c.recvline()
        flag_id = c.recvline()

        for count in range(0,4):
                c.recvline()

        c.close()
        return {"flag_id": flag_id + " " + token , "token": username + " " + password}

def genRndString():
        rang = randint(8,16)
        rndString = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(rang))
        return rndString
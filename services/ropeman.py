from pwn import *
from random import randint
import sys

def get_flag(host, port, flag_id, token):
        c = remote(host,port)
        for count in range(0,31):
                c.recvline()
        c.sendline("l")
        c.recvline()
        c.sendline(flag_id)
        c.recvline()
        c.sendline(token)
        c.recvline()
        c.recvline()
        c.recvline()
        c.recvline()
        data = c.recvline()
        c.sendline("x")
        c.close()
        return data.replace("Your status: [","").replace("]","").replace('\n',"")
        
def set_flag(host, port, flag):
        #print("flag set: " + flag)
        username = genRndString()
        password = genRndString()
        c = remote(host,port)
        for count in range(0,31):
                c.recvline()
        c.sendline("c")
        c.recvline()
        c.sendline(username)
        c.recvline()
        c.sendline(password)
        c.recvline()
        c.sendline("m")
        c.recvline()
        c.sendline(flag)
        c.recvline()
        c.sendline("x")
        c.close()
        return {"flag_id": username, "token": password}

def genRndString():
        rang = randint(8,16)
        rndString = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(rang))
        return rndString 

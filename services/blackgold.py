from pwn import *
from random import randint
import sys

def get_flag(host, port, flag_id, token):
        c = remote(host,port)
        for count in range(0,4):
                c.recvline()
        c.sendline("P")
        c.recvline()
        c.sendline(flag_id)
        c.sendline(token)
        data = c.recvline()
        c.close()
        return data.replace("Recipe content: ","").replace(" ","").replace('\n',"")
        
def set_flag(host, port, flag):
        #print("flag set: " + flag)
        flag_id = genFlagID()
        password = genRndString()
        c = remote(host,port)
        for count in range(0,4):
                c.recvline()
        c.sendline("A")
        c.recvline()
        c.sendline(flag_id)
        c.sendline(password)
        c.sendline(flag)
        c.recvline()
        c.close()
        return {"flag_id": flag_id, "token": password}

def genRndString():
        rang = randint(8,16)
        rndString = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(rang))
        return rndString 

def genFlagID():
        flag_id = randint(0,999999999)
        return str(flag_id)

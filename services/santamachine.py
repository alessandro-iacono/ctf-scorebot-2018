import socket
import sys
import pexpect
import pexpect.fdpexpect
import re
import random
from random import randint
import string
from pwn import *
import sys

class Service:
    def __init__(self, ip, port):
        if ip:
            self._conn = socket.create_connection((ip,port))
            self.child = pexpect.fdpexpect.fdspawn(self._conn.fileno())
        else:
            self._conn = None
            self.child = pexpect.spawn("../service/ro/santamachine")
            self.child.logfile = sys.stdout

    def get(self):
        return self.child

    def close(self):
        self.child.close()
        if self._conn:
            self._conn.close()

def get_flag(host, port, flag_id, token):
        service = Service(host, port)
        c = service.get()

        c.expect('\?')
        
        c.sendline("L")    
        
        c.expect("\password")
        
        tosend = flag_id + " " + token   
        
        c.sendline(tosend)
       				
        c.expect('\w+')
        c.sendline("L")
        
        options = [
        'Your letter to Santa is:\n\w+',
        'You must first write a letter to be able to read it.'
        ]
        match = c.expect(options)
        if match != 0:
            service.close()
            raise Exception(options[match])
		
        flag = re.search('^Your letter to Santa is:\n(\w+)$', c.after).group(1)

        service.close()

        return flag
        
def set_flag(host, port, flag):
        #print("flag set: " + flag)
        flag_id = genFlagID()
        password = genRndString()

        tosend = flag_id + " " + password   

        service = Service(host, port)
        c = service.get()
       
        c.expect('\?')
		
        c.sendline("R")
        
        c.expect("password")

        c.sendline(tosend);

        c.expect('saved!')
        
        service.close()
			
        service = Service(host, port)
        c = service.get()
        c.expect('\?')	
        c.sendline("L")
        c.expect("password")
        c.sendline(tosend)

        c.expect('reading responses.')
            
        c.sendline("W")
        
        c.expect('done.')
        c.sendline(flag)
        c.sendline("\n")
        
        c.expect('\.')
        c.close()

        return {"flag_id": flag_id, "token": password}

def genRndString():
        rang = randint(8,16)
        rndString = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(rang))
        return rndString 

def genFlagID():
        flag_id = randint(0,999999999)
        return str(flag_id)

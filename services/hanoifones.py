import socket
import sys
import pexpect
import pexpect.fdpexpect
import re
import random
from random import randint
import string
class Service:
    def __init__(self, ip, port):
        if ip:
            self._conn = socket.create_connection((ip,port))
            self.child = pexpect.fdpexpect.fdspawn(self._conn.fileno())
        else:
            self._conn = None
            self.child = pexpect.spawn("../service/ro/hanoiFones")
            self.child.logfile = sys.stdout

    def get(self):
        return self.child

    def close(self):
        self.child.close()
        if self._conn:
            self._conn.close()

def get_flag(ip, port, flag_id, token):
    service = Service(ip, port)
    c = service.get()

    c.expect('\?:')
    c.sendline('2')
    c.expect('Insert the auction ID:')
    c.sendline(flag_id)
    options = [
        'Insert the password:',
        'Auction does not exist'
    ]
    match = c.expect(options)
    if match != 0:
        service.close()
        raise Exception(options[match])

    c.sendline(token)
    options = [
        'Your IMEI: \w+',
        'Wrong password!'
    ]
    match = c.expect(options)
    if match != 0:
        service.close()
        raise Exception(options[match])
    flag = re.search('^Your IMEI: (\w+)$', c.after).group(1)

    c.expect('\?:')
    c.sendline('4')
    service.close()

    return flag


def set_flag(ip, port, flag):
    service = Service(ip, port)
    c = service.get()
    
    flag_id = genFlagID()
    password = genRndString()
    c.expect('\?:')
    c.sendline('1')
    c.expect('Insert the IMEI of the \(hano\)iFon:')
    c.sendline(flag)
    c.expect('Auction ID: \w+')
    flag_id = re.search('^Auction ID: (\w+)$', c.after).group(1)
    c.expect('Your Password: \w+')
    password = re.search('^Your Password: (\w+)$', c.after).group(1)
    c.expect('\?:')
    c.sendline('4')

    service.close()

    return {"flag_id": flag_id, "token": password}

def genRndString():
        rang = randint(8,16)
        rndString = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(rang))
        return rndString 

def genFlagID():
        flag_id = randint(0,999999999)
        return str(flag_id)

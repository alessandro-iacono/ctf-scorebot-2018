import sys
from lxml import html
import requests
import string

#import secrets
import random
from random import randint

def get_flag(host, port, flag_id, token):
    flag_url="%s:%s" % (flag_id, token)
    url="http://%s@%s:%s/intern/" % (flag_url, host, port)
    resp=requests.get(url).text
    flag_pos = string.find(resp, "FLG_")+4;
    flag = resp[flag_pos:]
    return flag

def set_flag(host, port, flag):
    flag = "FLG_"+flag
    flag_id = gen_flagID()
    token = gen_passwd()
    flag_url="username=%s&pass=%s&secret=%s" % (flag_id, token, flag)
    url="http://%s:%s/extern/register.html/registration" % (host, port)
    resp=requests.post(url, data={'username': flag_id, 'pass':token, 'secret':flag})
    return {'flag_id':flag_id, 'token':token}

def gen_passwd():
    rang=randint(10, 20)
    password=''.join(random.choice(string.ascii_letters + string.digits) for _ in range(rang))
    return password

def gen_flagID():
    flag_id = randint(0, 9999999999)
    return flag_id

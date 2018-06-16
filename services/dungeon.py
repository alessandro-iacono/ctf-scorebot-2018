import sys, socket
import time
from random import randint
from pwn import *

def get_flag(host, port, flag_id, token):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host, 20090))
	
	time.sleep(0.1)
	init_ack = s.recv(4096)
	
	s.send('2016\n')
	time.sleep(0.1)
	test_2016_ack = s.recv(4096)
	
	s.send('west\n')
	time.sleep(0.2)
	plane_ack = s.recv(4096)
	
	plane = ''

	if """'==.I\_____________..--"<__""" in plane_ack :
		plane = 'f16'

	if """-=========================='===^==^==^=====^==='=============================-""" in plane_ack :
		plane = 'f117'

	if """XXMMMMm8888888888888888888888888WWWMMMMMMMM""" in plane_ack :
		plane = 'sr71'

	s.send(plane+'\n')
	time.sleep(0.1)
	init_2_ack = s.recv(4096)
	
	s.send('east\n')
	time.sleep(0.1)
	dwarf_ack = s.recv(4096)

	s.send('2016\n')
	time.sleep(0.1)
	dwarf_fail_ack = s.recv(4096)
	s.send('east\n')
	time.sleep(0.1)
	auth_ack = s.recv(4096)

	s.send('1\n')
	time.sleep(0.1)
	auth_fail_ack = s.recv(4096)

	s.send('east\n')
	time.sleep(0.1)
	get_flag_ack = s.recv(4096)
	
	s.send('get ' + flag_id + '\n')
	time.sleep(0.1)
	pwd_ack = s.recv(4096)
	
	s.send(token + '\n')
	time.sleep(0.1)
	flag_ack = s.recv(4096)
	
	s.close()
	
	return (flag_ack.split()[3])
		
def set_flag(host, port, flag):
	flag_id = genRndString()
	password = genRndString()
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host, 20090))
	
	time.sleep(0.1)
	init_ack = s.recv(4096)
	
	s.send('2016\n')
	time.sleep(0.1)
	test_2016_ack = s.recv(4096)
	
	s.send('west\n')
	time.sleep(0.2)
	plane_ack = s.recv(4096)
	
	plane = ''

	if """'==.I\_____________..--"<__""" in plane_ack :
		plane = 'f16'

	if """-=========================='===^==^==^=====^==='=============================-""" in plane_ack :
		plane = 'f117'

	if """XXMMMMm8888888888888888888888888WWWMMMMMMMM""" in plane_ack :
		plane = 'sr71'

	s.send(plane+'\n')
	time.sleep(0.1)
	init_2_ack = s.recv(4096)
	
	s.send('east\n')
	time.sleep(0.1)
	dwarf_ack = s.recv(4096)

	s.send('2016\n')
	time.sleep(0.1)
	dwarf_fail_ack = s.recv(4096)
	
	s.send('east\n')
	time.sleep(0.1)
	auth_ack = s.recv(4096)

	s.send('1\n')
	time.sleep(0.1)
	auth_fail_ack = s.recv(4096)
	
	s.send('east\n')
	time.sleep(0.1)
	set_flag_ack = s.recv(4096)
	
	command = "store " + flag_id + " " + flag + " " + password + "\n"
	s.send(command)
	time.sleep(0.1)
	set_flag_ack = s.recv(4096)
	
	s.close()
	
	return {"flag_id": flag_id, "token": password}
		
def genRndString():
        rang = randint(8,16)
        rndString = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(rang))
        return rndString

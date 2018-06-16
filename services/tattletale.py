def get_flag(host, port, flag_id, token):

	#from socket import socket
	from telnetlib import Telnet

	def send_msg(t, msg):
		t.write(msg+'\n')

	def read_until_prompt(t):
		ans =t.read_until('getflag: ')
		return ans

	def do_checkflag(t, flag_id, token):
		send_msg(t, '3')
		send_msg(t, flag_id)
		send_msg(t, token)
		ans = read_until_prompt(t)
		flag = ans.split(' ')[-1].split()
		return flag


	flag = ''
	error = 0
	error_msg = ''
	try:
		t = Telnet(host,port)
		flag = do_checkflag(t, flag_id, token)[0]

		if flag == "getflag_auth_fail":
			error = 1 #up but not functional
			error_msg = flag
		elif flag == "no_entry_exists":
			error = 1 # up but not functional
			error_msg = flag
		t.close()   
	except Exception as e:
		error = -1
		error_msg = str(e)

	return flag
	
	
def set_flag(host, port, flag):

	from telnetlib import Telnet

	def get_random_flag_id():
		import random
		import string
		username = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(16))
		return username

	def get_random_token():
		import random
		import string
		return ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(16))

	
	def read_until_prompt(t):
		ans = t.read_until('setflag: ')
		return ans

	def send_msg(t, msg):
		t.write(msg+'\n') 

	def do_setflag(t, flag_id, token, flag):
		send_msg(t, '2')
		send_msg(t, flag_id)
		send_msg(t, token)
		send_msg(t, flag)
		ans = read_until_prompt(t)
		result = ans.split(' ')[-1].strip()
		return result

	flag_id = get_random_flag_id()
	token = get_random_token()
	error = 0
	error_msg = ''
	try:
		t = Telnet(host,port)
		ans = do_setflag(t, flag_id, token, flag)
		if ans == "flag_set":
			pass
		elif ans == "flag_updated":
			pass
		elif ans == "flag_update_auth_fail":
			error = 1 #up but not functional
			error_msg = ans
		else:
			error = -1 #down
			#error_msg = "setflag is broken or something, no confirmation recieved"
			error_msg = ans
	except Exception as e:
		error = -1
		error_msg = str(e)

	return {"flag_id": flag_id, "token": token}

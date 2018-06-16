import string
import random

class Service:
	def __init__(self, name, port, module):
		self.name = name
		self.port = port
		self.module = module
		self.flagList = {}
		self.argList = {}

	def setFlag(self, host, teamName):
		try:	
			flag = "".join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))
			flag_64 = flag.encode('base64')
			self.argList[teamName] = self.module.set_flag(host, self.port, flag_64)
			self.flagList[teamName] = flag
			print "[-] Set Flag To " + self.name + " Service for " + teamName + " Team"
		except Exception:
			pass

	def getFlag(self, host, teamName):
		try:
			flag_id = self.argList[teamName]["flag_id"]
			token = self.argList[teamName]["token"]
			flag_64 = self.module.get_flag(host, self.port, flag_id, token)
			flag = flag_64.decode('base64')
			print "[-] Retrieve Flag to " + self.name + " Service for " + teamName + " Team"
			return flag
		except Exception:
			pass

	def getFlagID(self, teamName):
		return (argList[teamName]).get("flag_id", None)

from pwn import *
import time
import socket

class Game:
	def __init__(self, teamList, serviceList, honeypotList):
		self.teamList = teamList
		self.serviceList = serviceList
		self.honeypotList = honeypotList

	def setFlags(self, teamListStatus):
		for serviceName, service in self.serviceList.iteritems():
			for teamName, team in self.teamList.iteritems():
				try:
					c = remote(team.host, service.port)
					c.close()
					teamListStatus[teamName][serviceName] = "Up"
					service.setFlag(team.host, teamName)
				except Exception:
					print '[!] Service %s is Not responding... No Defense Point for %s' % (serviceName, teamName)
					teamListStatus[teamName][serviceName] = "Down"

	def getFlags(self):
		for serviceName, service in self.serviceList.iteritems():
			if serviceName not in self.honeypotList:
				for teamName, team in self.teamList.iteritems():
					try:
						tempFlag = service.getFlag(team.host, teamName)
						if tempFlag == service.flagList[team.name]:
							print "[+] Defense Point! +1 for %s - %s" % (teamName, serviceName)
							team.updateDefenseScore(1)
					except socket.error:
						print '[!] Service %s is Not responding... No Defense Point for %s' % (serviceName, teamName)
					except Exception:
						pass

	def resetLog(self):
		outFile = open("log.txt", "w")
		outFile.write("")
		outFile.close()

	def restoreLog(self):
		try:
			inFile = open("log.txt", "r")
			inText = inFile.read()
			inFile.close()
			if inText == "":
				return
			i = len(inText) - 5
			j = len(inText)
			while inText[i : j] != "Local":
				i = i - 1
				j = j - 1
			for teamName, team in self.teamList.iteritems():
				j = i + len(teamName)
				while inText[i : j] != teamName:
					i = i + 1
					j = j + 1
				j = i + len("Attack Points: ")
				while inText[i : j] != "Attack Points: ":
					i = i + 1
					j = j + 1
				s = inText[j]
				while inText[j] != "\n":
					j = j + 1
					s = s + inText[j]
				team.attackScore = int(s)
				j = i + len("Defense Points: ")
				while inText[i : j] != "Defense Points: ":
					i = i + 1
					j = j + 1
				s = inText[j]
				while inText[j] != "\n":
					j = j + 1
					s = s + inText[j]
				team.defenseScore = int(s)
				print "restoreLog => " + teamName + ": Attack Points:" + str(team.attackScore) + " & Defense Points:" + str(team.defenseScore)
		except Exception:
			pass

	def updateLog(self):
		localTime = time.asctime(time.localtime(time.time()))
		outFile = open("log.txt","a")
		outText = "\n--------------------\nLocal Time: " + str(localTime)
		for teamName, team in self.teamList.iteritems():
			outText += "\n--------------------\n" + teamName + "\nAttack Points: " + str(team.attackScore) + "\nDefense Points: " + str(team.defenseScore)
		outFile.write(outText + "\n")
		outFile.close()

	def submitFlags(self, teamName, serviceName, flag):
		team = self.teamList[teamName]
		flagList = self.serviceList[serviceName].flagList
		for user, userFlag in flagList.iteritems():
			if flag == userFlag and flag != "" and serviceName not in self.honeypotList:
				print '[+] Attack Point! +2 for ' + teamName
				team.updateAttackScore(2)
				self.serviceList[serviceName].flagList[user] = ""
				return "Flag Valid!\n"
			elif flag == userFlag and flag != "" and serviceName in self.honeypotList:
				print '[+] Ooops! Attack Point! -5 for ' + teamName
				team.updateAttackScore(-5)
				self.serviceList[serviceName].flagList[user] = ""
				phrases = ["That's strange. It worked, but it seems that was almost too easy... I'll go check my points.\n", 
							"Yeah! It was like stealing candies from a kid! :)\n\n\nOr was it?"]
				return phrases[random.randint(0, len(phrases) - 1)]
		return "Flag Invalid!\n"

	def getFlagID(self, serviceName, evilTeam):
		return self.serviceList[serviceName].argList[evilTeam].get("flag_id")

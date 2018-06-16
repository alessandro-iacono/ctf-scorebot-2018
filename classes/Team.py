class Team:
	def __init__(self, name, host, picture):
		self.name = name
		self.host = host
		self.picture = picture
		self.attackScore = 0
		self.defenseScore = 0

	def updateAttackScore(self, points):
		self.attackScore += points

	def updateDefenseScore(self, points):
		self.defenseScore += points

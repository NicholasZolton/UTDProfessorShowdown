from ratemyprof_api import RMPHolder

class Professor:
	def __init__(self, name, data):
		self.name = name
		self.rmpName = name
		# formatting rmp name
		lastName = self.rmpName[0:self.rmpName.find(',')]
		self.rmpName = self.rmpName[self.rmpName.find(',')+2:]
		if self.rmpName.find(' ') != -1:
			firstName = self.rmpName[0:self.rmpName.find(' ')]
		else:
			firstName = self.rmpName
		self.rmpNameReverse = lastName + ' ' + firstName
		self.rmpName = firstName + ' ' + lastName
		# end formatting
		self.data = data
		self.classNum = len(data)
		self.studentCount = 0 # number not dropped
		self.dropCount = 0 # number withdrawed or incomplete
		self.failCount = 0 # number failed (F)
		# convert letter to number grades
		self.conv = {
			"A+": 100,
			"A": 95,
			"A-": 92,
			"B+": 88,
			"B": 85,
			"B-": 82,
			"C+": 78,
			"C": 75,
			"C-": 72,
			"D+": 68,
			"D": 65,
			"D-": 62,
			"F": 40,
			"I": 1,
			"W": 0
		}
		# calculate median
		self.comb = []
		for i in self.data:
			if 'F' in i["grades"]:
				self.failCount += int(i["grades"]["F"])
			# print(i["term"] + ' ' + i["sect"] + ' ' + i["prof"])
			for j in i["grades"]:
				if j != "W" and j != "I":
					self.studentCount += int(i["grades"][j])
					for a in range(int(i["grades"][j])):
						self.comb.append(self.conv[j])
				else:
					if 'W' in i["grades"]:
						self.dropCount += int(i["grades"]["W"])
					if 'I' in i["grades"]:
						self.dropCount += int(i["grades"]["I"])
		self.comb.sort()
		# calculate % failed
		if self.studentCount == 0:
			self.studentCount = 1

		# Rate My Professor attributes
		self.trueRating = 0
		self.rmpRating = RMPHolder.x.ReturnProfessorDetail(self.rmpName, "overall_rating")
		if self.rmpRating == "error":
			self.rmpRating = RMPHolder.x.ReturnProfessorDetail(self.rmpNameReverse, "overall_rating")
		if self.rmpRating != "error" and self.rmpRating != 'N/A':
			self.rmpRating = float(self.rmpRating)
		else:
			self.rmpRating = -1
		if self.rmpRating != -1:
			if self.classNum >= 3:
				self.trueRating = (2/5)*(self.rmpRating*20) + (3/5)*(self.getMedian())
			elif self.classNum >= 2:
				self.trueRating = (3/5)*(self.rmpRating*20) + (2/5)*(self.getMedian())
			elif self.classNum >= 1:
				self.trueRating = (4/5)*(self.rmpRating*20) + (1/5)*(self.getMedian())
		else:
			if self.classNum >= 3:
				self.trueRating = (2 / 5) * (2.5 * 20) + (3 / 5) * (self.getMedian())
			elif self.classNum >= 2:
				self.trueRating = (3 / 5) * (2.5 * 20) + (2 / 5) * (self.getMedian())
			elif self.classNum >= 1:
				self.trueRating = (4 / 5) * (2.5 * 20) + (1 / 5) * (self.getMedian())


	def getMedian(self):
		return self.comb[int(len(self.comb) / 2)]

	def getPercentFailed(self):
		return self.failCount / self.studentCount

	def getPercentDropped(self):
		return self.dropCount / (self.studentCount + self.dropCount)

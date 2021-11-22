import json
import os
import json

from Professor import Professor


class Grades:
	# should be "trueRating", "rmpRating", or "median"
	sortType = "trueRating"

	def __init__(self, prefix, num):
		self.num = num
		self.prefix = prefix.upper()
		self.data = []
		self.bigData = []
		print("num -1")

		for file in os.listdir('./data/JSONS/'):
			gradesFile = open('./data/JSONS/' + file)
			self.source = json.load(gradesFile)
			# print(file)
			for i in self.source:
				# print(file + num)
				if 'num' in i:
					if i['num'] == num:
						self.bigData.append(i)
		print("num 0")

		self.namesList = []
		# create list of all unique names
		for i in self.bigData:
			if i["prof"] not in self.namesList and i['subj'] == self.prefix:  # TODO: Find out why this scuffed fix works
				# print(i)
				self.namesList.append(i["prof"])
		print("num 1")

		# for each professor
		for name in self.namesList:
			prof = []
			# go thru class list and add each class to the prof classes
			for i in self.bigData:
				if i["prof"] == name:
					prof.append(i)
			# create prof object
			p = Professor(name, prof)
			self.data.append(p)
		print("num 2")

		# sort the professors
		self.sortedProfsByTrueRating = sorted(self.data, key=lambda x: x.trueRating, reverse=True)
		self.sortedProfsByRMP = sorted(self.data, key=lambda x: x.rmpRating, reverse=True)
		self.sortedProfsByMedian = sorted(self.data, key=lambda x: x.getMedian(), reverse=True)
		print("num 3")

	def printProfs(self):
		for i in self.data:
			print(i["prof"])

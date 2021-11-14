import requests
import json


def searchCourseProfessors(courseNum=2305, profNames=['Chin']):
	baseurl = 'http://api.utdnebula.com/'
	header = {"Authorization": "dd1h55UQUb8x5nQIPW2iJ1ABaIDx9iv7"}
	queryurl = baseurl + '/v1/sections/search?course_number=' + courseNum
	response = requests.get(queryurl, headers=header)
	profSet = set([])

	for i in response.json():
		boolTest = False
		for j in profNames:
			if j in i['instructors']:
				boolTest = True
		if boolTest:
			profSet.add(i['instructors'])

	print(profSet)


def getCourseNameWithNumber(coursePrefix='cs', courseNum=2305):
	coursePrefix = coursePrefix.lower()
	baseurl = 'http://api.utdnebula.com/'
	header = {'Authorization': 'dd1h55UQUb8x5nQIPW2iJ1ABaIDx9iv7'}
	queryurl = baseurl + '/v1/sections/search?course_number=' + str(courseNum)
	response = requests.get(queryurl, headers=header)

	for i in response.json():
		if i['course_prefix'] == coursePrefix:
			return i['title']

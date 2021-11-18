# Author: Rodantny Reyes
# License: MIT license
# Source: https://github.com/Rodantny/Rate-My-Professor-Scraper-and-Search

import os.path

import requests
import json
import math

class RateMyProfScraper:
    def __init__(self,schoolid):
        self.UniversityId = schoolid
        if os.path.exists('./data/profData.dat'):
            self.professorlist = self.readFromFile()
        else:
            self.professorlist = self.createprofessorlist()
        self.indexnumber = False

    def saveToFile(self):
        listFile = open("./data/profData.dat", 'w')
        for i in self.professorlist:
            listFile.write(json.dumps(i) + '\n')
        listFile.close()

    def readFromFile(self):
        listFile = open('./data/profData.dat', 'r')
        tempProfList = []
        with open('./data/profData.dat', 'r') as f:
            lines = f.readlines()

        for line in lines:
            tempProfList.append(json.loads(line))

        self.professorlist = tempProfList
        return tempProfList

    def createprofessorlist(self):#creates List object that include basic information on all Professors from the IDed University
        print('rewriting prof data json')
        tempprofessorlist = []
        num_of_prof = self.GetNumOfProfessors(self.UniversityId)
        num_of_pages = math.ceil(num_of_prof / 20)
        i = 1
        while (i <= num_of_pages):# the loop insert all professor into list
            page = requests.get("http://www.ratemyprofessors.com/filter/professor/?&page=" + str(
                i) + "&filter=teacherlastname_sort_s+asc&query=*%3A*&queryoption=TEACHER&queryBy=schoolId&sid=" + str(
                self.UniversityId))
            temp_jsonpage = json.loads(page.content)
            temp_list = temp_jsonpage['professors']
            tempprofessorlist.extend(temp_list)
            i += 1
        return tempprofessorlist

    def GetNumOfProfessors(self,id):  # function returns the number of professors in the university of the given ID.
        page = requests.get(
            "http://www.ratemyprofessors.com/filter/professor/?&page=1&filter=teacherlastname_sort_s+asc&query=*%3A*&queryoption=TEACHER&queryBy=schoolId&sid=" + str(
                id))  # get request for page
        temp_jsonpage = json.loads(page.content)
        num_of_prof = temp_jsonpage[
                          'remaining'] + 20  # get the number of professors at William Paterson University
        return num_of_prof

    def SearchProfessor(self, ProfessorName):
        # lastName = ProfessorName[0:ProfessorName.find(',')]
        # ProfessorName = ProfessorName[ProfessorName.find(',')+1:]
        # renamedName = ProfessorName[ProfessorName.find(' ')+1:] + ProfessorName[0:ProfessorName.find(",")]
        # print(renamedName)
        self.indexnumber = self.GetProfessorIndex(ProfessorName)
        # self.PrintProfessorInfo()
        return self.indexnumber

    def GetProfessorIndex(self,ProfessorName):  # function searches for professor in list
        for i in range(0, len(self.professorlist)):
            if ProfessorName == (self.professorlist[i]['tFname'] + " " + self.professorlist[i]['tLname']):
                return i
        return False  # Return False is not found

    def PrintProfessorInfo(self):  # print search professor's name and RMP score
        if self.indexnumber == False:
            print("error")
        else:
            print(self.professorlist[self.indexnumber])

    def PrintProfessorDetail(self,key):  # print search professor's name and RMP score
        if self.indexnumber == False:
            # print("error")
            return "error"
        else:
            # print(self.professorlist[self.indexnumber][key])
            return self.professorlist[self.indexnumber][key]

    def ReturnProfessorDetail(self, profname, property):
        self.SearchProfessor(profname)
        return self.PrintProfessorDetail(property)

# this is a working example of grabbing a professor's overall rating
# UTDUniv = RateMyProfScraper(1273)
# UTDUniv.SearchProfessor("Jason Smith")
# UTDUniv.PrintProfessorDetail("overall_rating")
# UTDUniv.saveToFile()

class RMPHolder:
    x = RateMyProfScraper(1273)

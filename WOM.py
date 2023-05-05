import requests #pip install requests
import csv
import pandas as pd #pip install pandas
from io import StringIO

#WOM
class WOMcomp:
	
    def __init__(self, id):
        self.id = id
        
    
    def makeAPIUrl(self, skill):
        self.url = "https://api.wiseoldman.net/v2/competitions/" + str(self.id) + "/csv?table=teams&metric=" + skill

    def getWOMData(self, skill):
        self.makeAPIUrl(skill)
        DataApi = requests.get(self.url)
        if DataApi.status_code == 200:
            '''convert data into list of lines'''
            print("api data imported")
            DataStr = DataApi.text
            DataList = DataStr.splitlines()
            DataTeamLists = []
            '''remove header and add data in WOMCompTeamData'''
            Lines = len(DataList)
            
            for Line in range(Lines):
                if Line != 0:
                    tempList = DataList[Line].split(",")
                    DataTeamLists.append(WOMCompTeamData(tempList[0], tempList[1], tempList[2], tempList[3], tempList[4], tempList[5], skill))
            self.DataTeamLists = DataTeamLists
        else:
            print("error: api data was wrong")
    
    def getWOMTeamData(self, DataTeamLists, teamName):
        Lines = len(DataTeamLists)
        for Line in range(Lines):
            if DataTeamLists[Line].teamName == teamName:
                print("teamdata collected from " + DataTeamLists[Line].teamName)
                self.teamdata = DataTeamLists[Line]



class WOMCompTeamData:
    def __init__(self, rank, teamName, PlayerAmount, TotalXP, AvgXP, MVP, skill):
        self.rank = rank
        self.teamName = teamName
        self.PlayerAmount = PlayerAmount
        self.TotalXP = TotalXP
        self.AvgXP = AvgXP
        self.MVP = MVP
        self.skill = skill
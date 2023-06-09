import requests #pip install requests
import csv
import pandas as pd #pip install pandas
from io import StringIO
import time

#WOM
class WOMcomp:
	
    def __init__(self, id:str):
        self.id = id
        
    
    def makeAPIUrl(self, skill:str):
        self.url = "https://api.wiseoldman.net/v2/competitions/{self.id:str}/csv?table=teams&metric={skill:str}"

    def getData(self, skill:str):
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
    
    def getTeamData(self, DataTeamLists, teamName):
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

class WOMGroup:
    
    def __init__(self, id:str):
        self.id = id
        

    # function to update user
    def updateUser(self, user:str, data:pd.DataFrame = []):
        assert type(user) is str
        time.sleep(1.5)
        print('{user} ({row}/{ttl})'.format(user=user,
                                            row=data.u_count.loc[user] + 1,
                                            ttl=data.u_count.max() + 1))
        try:
            r = requests.post('https://api.wiseoldman.net/v2/players/{}'.format(user), timeout=10)
            print('status: {}'.format(r.status_code))
        except requests.ReadTimeout as t:
            print('Timeout Error')
            return 408

    def updateGroup(self):
        # Get list of users
        users = []
        tmp_r = requests.get('https://api.wiseoldman.net/v2/groups/{}'.format(self.id))
        tmp_j = tmp_r.json()
        tmp_m = [x['player']['username'] for x in tmp_j['memberships']]
        users += tmp_m 
        users = pd.DataFrame(pd.Series(users).unique(), columns=['user'])
        users['u_count'] = users.index
        users = users.set_index('user')
        for x in users.index.tolist():
            self.__class__.updateUser(self,x, users)
            


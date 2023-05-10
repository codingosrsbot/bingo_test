import os
from PIL import Image #pip install pillow
from io import BytesIO
import discord #pip install discord.py
from discord.ext import commands
import json




#loading assets
with open("./config/tiles.json", 'r') as f:
    bingoTilesJson = json.load(f)
    
with open("./config/topsecret.json", 'r') as f:
    secretTilesjson = json.load(f)

with open("./config/bingoConfig.json", 'r') as f:
    bingoConfigJson = json.load(f)
    bingoAdminRole = bingoConfigJson['admin role']
    bingoOrganizerid = bingoConfigJson['organizer id']


#functions
def startup():
    loadAllBingoBoards()
    for x in boardsData:
        tmpTeam = x['Team name']
        tmpBoardData = x['Board data']
        tmpBoard = BingoBoard(tmpTeam, tmpBoardData)
        bingoBoards.append(tmpBoard)

    

def loadAllBingoBoards():
    boardsData.clear()
    root_dir = str(f"./teams/")
    # iterate through all subdirectories in the root directory
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # iterate through all filenames in the current subdirectory
        for filename in filenames:
            if filename == "Board.json":
                board_path = os.path.join(dirpath, filename)
                with open(board_path, "r") as f:
                    board_data = json.load(f)
                teamName = dirpath.removeprefix("./teams/")
                tmpList = {'Team name': teamName, 'Board data': board_data}
                boardsData.append(tmpList)
    print(boardsData)
    saveBingoBoard("totaal", boardsData)

def createBingoBoard(team):
    board = bingoTilesJson
    saveBingoBoard(team, board)

def saveAllBingoBoards():
    for x in boardsData:
        team = x['Team name']
        data = x['Board data']
        fpath = str(f"./teams/{team}")
        if not os.path.exists(fpath):
            os.makedirs(fpath)
        with open(f"{fpath}/Board.json", 'w') as f:
            json.dump(data, f, indent=4)

def saveBingoBoard(team, board):
    fpath = str(f"./teams/{team}")
    if not os.path.exists(fpath):
        os.makedirs(fpath)
    with open(f"{fpath}/Board.json", 'w') as f:
        json.dump(board, f, indent=4)

def getBoard(team):
    for x in boardsData:
        if team == x["Team name"]:
            return x

def addBingoTilesToBoard(boardData):
    tmpBoard = []
    for x in boardData:
        tmpTile = BingoTile(x)
        tmpTileData = tmpTile.getTileData()
        print(tmpTileData)
        tmpBoard.append(tmpTileData)
        print(tmpBoard)
        return tmpBoard

def getAllTaskDescriptions(board):
	descriptions = []
	for x in board:
			match x['type']:
				case "evidence":
					descriptions.append(x['description'])
				case "subtile evidence":
					for y in x['type specific']['subtiles']:
						descriptions.append(y['description'])
				case "subtile set evidence":
					for y in x['type specific']['subtileset']:
						for z in y['subtiles']: 
							descriptions.append(z['description'])
				case "count":
					print("count")
				case "set count":
					print("set count")
				case "xp":
					print("xp")                                                                         
	return descriptions

async def isBingoTaskApproved(payload):
    channel = await bot.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    guild = bot.get_guild(payload.guild_id)
    user = guild.get_member(payload.user_id)
    roles = user.roles
    for descr in bingoDescriptions:	
        if message.content == str(descr) and str(payload.emoji) == '✅' and user != message.author:
            role = discord.utils.get(roles, name= str(bingoAdminRole))
            if role is not None:
                await channel.send(f"{user.name} approved {str(descr)}")
            else:
                await channel.send(f'{user.name} you are not an admin!')
        if message.content == str(descr) and str(payload.emoji) == '🏴󠁧󠁢󠁳󠁣󠁴󠁿'and user != message.author:
            if str(payload.user_id) == str(bingoOrganizerid) :
                await channel.send(f'{user.name} is the best')
            else: 
                await channel.send(f'{user.name} stop pretending to be in charge')

async def isBingoTaskUnapproved(payload):
    channel = await bot.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    guild = bot.get_guild(payload.guild_id)
    user = guild.get_member(payload.user_id)
    roles = user.roles
    for descr in bingoDescriptions:	
        if message.content == str(descr) and str(payload.emoji) == '✅' and user != message.author:
            role = discord.utils.get(roles, name= str(bingoAdminRole))
            if role is not None:
                await channel.send(f"{user.name} removed approval {str(descr)}")
            else:
                await channel.send(f'{user.name} you are not an admin!')
        if message.content == str(descr) and str(payload.emoji) == '🏴󠁧󠁢󠁳󠁣󠁴󠁿'and user != message.author:
            if str(payload.user_id) == str(bingoOrganizerid) :
                await channel.send(f'{user.name} is the best (removed objection)')
            else: 
                await channel.send(f'{user.name} stop pretending to be in charge')

#init
bot = []
boardsData = []
bingoBoards = []

bingoDescriptions = getAllTaskDescriptions(bingoTilesJson)

class BingoBoard():
    def __init__(self, team, data):
            self.team = team
            self.data = data
    
    def getBoardTeam(self):
        return self.team

    def getBoardData(self):
        return self.data
        


    

class BingoTile(BingoBoard):
    def __init__(self, team, data):
        self.data = team
        self.data = data
        match self.data['type']:
            case "evidence":
                self.typeSpecific = []
            case "subtile evidence":
                self.typeSpecific = evidenceSubtile(self)
            case "subtile set evidence":
                self.typeSpecific = evidenceSubtile(self)
            case "count":
                print("count")
            case "set count":
                print("set count")
            case "xp":
                print("xp") 

    def getTileData(self):
         print(self.data)
         return list(self.data)   

    def getTileName(self):
        return self.data['name']

    def getTileDescription(self):
        return self.data['escription']
    
    def getTileType(self):
        return self.data['type']

    def getTileCompleted(self):
        return self.data['completed']

    def setTileCompleted(self):
        self.data['completed'] += 1

    def removeTileCompleted(self):
        self.data['completed'] -= 1
    
    def setTileCompleted(self, amount):
        self.data['completed'] = amount
    
    def isTileOverruled(self):
        return self.data['overruled']

    def setTileOverruled(self):
        self.data['overruled'] = True

    def removeTileOverruled(self):
        self.data['overruled'] = False

    def getTileRow(self):
        return self.data['row']
    
    def getTileRow(self):
        return self.data['column']
         

class evidenceSubtile(BingoTile):
    def __init__(self, data):
        self.data = data
        type = self.data.type
        match type: 
            case "subtile evidence":
                self.subtile = self.data['type specific']['subtiles']
            case "subtile set evidence": 
                self.subtile = self.data['type specific']['subtileset']['subtiles']

    def getEvidenceSubtileDescription(self):
        return self.subtile['description']

    def getEvidenceSubtileCompleted(self):
        return self.subtile['completed']

    def setEvidenceSubtileCompleted(self):
        match type: 
            case "subtile evidence":
                self.data['type specific']['subtiles']['completed'] += 1
                self.subtile = self.data['type specific']['subtiles']
            case "subtile set evidence": 
                self.data['type specific']['subtileset']['subtiles']['completed'] += 1
                self.subtile = self.data['type specific']['subtileset']['subtiles']

    def removeEvidenceSubtileCompleted(self):
        match type: 
            case "subtile evidence":
                self.data['type specific']['subtiles']['completed'] -= 1
                self.subtile = self.data['type specific']['subtiles']
            case "subtile set evidence": 
                self.data['type specific']['subtileset']['subtiles']['completed'] -= 1
                self.subtile = self.data['type specific']['subtileset']['subtiles']

    def isEvidenceSubtileOverruled(self):
        return self.subtile['overruled']

    def areSubtilesCompleted(self):
        tmpCompleted = 0
        for x in self.subtile:
            if x['completed'] != 0 and x['overruled'] == False:
                tmpCompleted = 1
            super(evidenceSubtile, self).setTileCompleted(tmpCompleted)

    

               






























































































































class BingoBoardOld:
    row = 5
    col = 5
    def __init__(self): 
        self.CSBBoard = []
        self.CSBBoard.append(BingoTile(0,0,"magican effect", "NA", "xp", False))
        self.CSBBoard.append(BingoTile(0,1,"feeling coy", "NA", "evidence", False))
        self.CSBBoard.append(BingoTile(0,2,"brrrrrr", "NA", "xp", False))
        self.CSBBoard.append(BingoTile(0,3,"secret", "NA", "xp", False))
        self.CSBBoard.append(BingoTile(0,4,"don't get pked", "NA", "xp", False))
        self.CSBBoard.append(BingoTile(1,0,"robot wars", "NA", "xp", False))
        self.CSBBoard.append(BingoTile(1,1,"secret", "NA", "xp", False))
        self.CSBBoard.append(BingoTile(1,2,"for eggy", "NA", "xp", False))
        self.CSBBoard.append(BingoTile(1,3,"stale as ol as time", "NA", "xp", False))
        self.CSBBoard.append(BingoTile(1,4,"test your luck", "NA", "evidence", False))
        self.CSBBoard.append(BingoTile(2,0,"sorry ladies", "NA", "xp", False))
        self.CSBBoard.append(BingoTile(2,1,"make that dolla", "NA", "xp", False))
        self.CSBBoard.append(BingoTile(2,2,"secret", "NA", "xp", False))
        self.CSBBoard.append(BingoTile(2,3,"dragon deez", "NA", "xp", False))
        self.CSBBoard.append(BingoTile(2,4,"see you around", "NA", "xp", False))
        self.CSBBoard.append(BingoTile(3,0,"everyone's favourite boss", "NA", "xp", False))
        self.CSBBoard.append(BingoTile(3,1,"secret", "NA", "xp", False))
        self.CSBBoard.append(BingoTile(3,2,"say shat you want about me", "NA", "xp", False))
        self.CSBBoard.append(BingoTile(3,3,"secret", "NA", "evidence", False))
        self.CSBBoard.append(BingoTile(3,4,"for our osaat pals", "NA", "xp", False))
        self.CSBBoard.append(BingoTile(4,0,"secret", "NA", "xp", False))
        self.CSBBoard.append(BingoTile(4,1,"you like my hair?", "NA", "xp", False))
        self.CSBBoard.append(BingoTile(4,2,"peeporun", "NA", "xp", False))
        self.CSBBoard.append(BingoTile(4,3,"most requested boss", "NA", "xp", False))
        self.CSBBoard.append(BingoTile(4,4,"secret", "NA", "xp", False))

 
    def setCompletedTileTrue(self, row, col):
        pos = row * self.row + col
        print(pos)
        self.CSBBoard[pos].completed = True

    async def fillBoard(self, ctx):
        boardsize = (1428,2000)
        completesize = (200,200)
        tilesize = (286,232)
        boardstartpoint = (0,600)

        backgound = Image.open('./img/board.png')
        overlay = Image.open('./img/complete.png')
        overlay = overlay.resize(completesize)
        boardImg = backgound.copy()
        i = 0
        for i in range(self.row):
            for j in range(self.col):
                pos = i * self.row + j
                if self.CSBBoard[pos].completed:
                    print("pos is " + str(pos))
                    print("i is " + str(i))
                    print("j is " + str(j))
                    print(self.CSBBoard[pos].name)
                    boardImg.paste(overlay, (43+(j*286),610+(i*232)), overlay)
        bytes = BytesIO()
        boardImg.save(bytes, format="PNG")
        bytes.seek(0)
        dBoard = discord.File(bytes, filename="boardImg.png")

        await ctx.send("your board", file=dBoard)
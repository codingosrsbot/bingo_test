from PIL import Image #pip install pillow
from io import BytesIO
import discord #pip install discord.py
from discord.ext import commands
'''
Tile = [
    "name" : ""
    "description" : ""
    "type" : ""
    "complete" : ""
    "row" : ""
    "column" : ""
    ]

'''









class BingoTile:
    def __init__(self, row, col, name, descrip, type, completed):
        self.row = row
        self.col = col
        self.name = name
        self.descrip = descrip
        self.type = type #xp or evidence
        self.completed = completed


class BingoBoard:
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
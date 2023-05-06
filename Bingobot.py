
import discord #pip install discord.py
from discord.ext import commands
import asyncio
import logging
import os.path


import WOM
import Bingo


# Settings

with open("Token.txt", 'r') as fp:
    gTOKEN = fp.readline()
    
# Bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

description = '''Discord osrs bot'''
bot = commands.Bot(intents=intents, command_prefix= "<" , description='Bingo time',  case_insensitive=True)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def woodcutmvp(ctx: discord.ext.commands.Context):
	id = 24073
	teamName = "special people"
	skill = "woodcutting"
	BingoComp = WOM.WOMcomp(id)
	BingoComp.getWOMData(skill)
	BingoComp.getWOMTeamData(BingoComp.DataTeamLists, teamName)
	print(BingoComp.teamdata.teamName + " asked " + skill +" mvp")
	await ctx.send("The " + skill  + " mvp of " + BingoComp.teamdata.teamName + " is ... " + BingoComp.teamdata.MVP)
	
@bot.command()
async def woodcutxp(ctx: discord.ext.commands.Context):
	id = 24073
	teamName = "special people"
	skill = "woodcutting"
	BingoComp = WOM.WOMcomp(id)
	BingoComp.getWOMData(skill)
	BingoComp.getWOMTeamData(BingoComp.DataTeamLists, teamName)
	print(BingoComp.teamdata.teamName + " asked " + skill +" xp")
	await ctx.send("The " + skill  + " xp of " + BingoComp.teamdata.teamName + " is ... " + BingoComp.teamdata.TotalXP)
        
@bot.command()
async def board(ctx: discord.ext.commands.Context):
	board = Bingo.BingoBoard()
	board.setCompletedTileTrue(2,3)
	board.setCompletedTileTrue(0,0)
	board.setCompletedTileTrue(4,4)
	board.setCompletedTileTrue(3,1)
	await board.fillBoard(ctx)
	
logging.basicConfig(level=logging.DEBUG)

bot.run(gTOKEN)

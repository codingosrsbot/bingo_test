
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
 
with open("WOM.txt", 'r') as fp:
    WOMid = fp.readline().rstrip('\n')
    WOMvc = fp.readline().rstrip('\n')
    print(WOMid)
    print(WOMvc)

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
async def ping(ctx: discord.ext.commands.Context):
	""" testing """
	author = str(ctx.author.id)
	logging.info(f"ping() from '{author}'")
	await ctx.send("pong")


@bot.command()
async def makeTeam(ctx: discord.ext.commands.Context, team:str):
	if discord.utils.get(ctx.author.roles, name="Bingo admin") is not None:
		await ctx.send("i'll make you a team <3")
		if team is not None:
			role = await ctx.guild.create_role(name="Bingo team: " + team)
			await ctx.send(team + " is created")
		else:
			await ctx.send("what team?")
	else:
		await ctx.send("Nice try!")
		


@bot.command()
async def woodcutmvp(ctx: discord.ext.commands.Context):
	teamName = "special people"
	skill = "woodcutting"
	BingoComp = WOM.WOMcomp(WOMid)
	BingoComp.getWOMData(skill)
	BingoComp.getWOMTeamData(BingoComp.DataTeamLists, teamName)
	print(BingoComp.teamdata.teamName + " asked " + skill +" mvp")
	await ctx.send("The " + skill  + " mvp of " + BingoComp.teamdata.teamName + " is ... " + BingoComp.teamdata.MVP)
	
@bot.command()
async def woodcutxp(ctx: discord.ext.commands.Context):
	id = 24073
	teamName = "special people"
	skill = "woodcutting"
	BingoComp = WOM.WOMcomp(WOMid)
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

@bot.command()
async def update(ctx: discord.ext.commands.Context):
	WOM.WOMCompUpdate(WOMid, WOMvc)
	await ctx.send("wom updated maybe")
	
logging.basicConfig(level=logging.DEBUG)

bot.run(gTOKEN)
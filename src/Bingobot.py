import discord #pip install discord.py
from discord.ext import commands, tasks
import asyncio
import logging
import os.path
import json

import WOM
import Bingo


# Settings

with open("./config/Token.txt", 'r') as fp:
    gTOKEN = fp.readline()
 
with open("./config/WOMConfig.json", 'r') as f:
    WOMjson = json.load(f)
    WOMid = WOMjson['competition id']
    WOMgid = WOMjson['group id']
    
WOMg = WOM.WOMGroup(WOMgid)    
allBingoBoards = []

# Bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True

description = '''Discord osrs bot'''
bot = commands.Bot(intents=intents, command_prefix= "<" , description='Bingo time',  case_insensitive=True)

def getBot():
	return bot


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    myIntervalTasks.start()
    Bingo.bot = bot
    Bingo.startup()
    
@bot.event
async def on_raw_reaction_add(payload):
	await Bingo.isBingoTaskApproved(payload)

@bot.event
async def on_raw_reaction_remove(payload):
	await Bingo.isBingoTaskUnapproved(payload)

@tasks.loop(seconds=3600)
async def myIntervalTasks():
	print("WOM gorup updating")
	#WOMg.updateGroup()
	#update skill tiles from every team
 

@bot.command()
async def ping(ctx: discord.ext.commands.Context):
	""" testing """
	author = str(ctx.author.id)
	logging.info(f"ping() from '{author}'")
	await ctx.send("pong")


@bot.command()
async def makeTeam(ctx: discord.ext.commands.Context, team:str):
	if discord.utils.get(ctx.author.roles, name=str(Bingo.bingoAdminRole)) is not None:
		await ctx.send("i'll make you a team <3")
		if team is not None:
			role = await ctx.guild.create_role(name="Bingo team: {team:str}")
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
	BingoComp.getData(skill)
	BingoComp.getTeamData(BingoComp.DataTeamLists, teamName)
	print("{BingoComp.teamdata.teamName:str} asked {strskill:str} mvp")
	await ctx.send("The {skill:str} mvp of {BingoComp.teamdata.teamName:str} is ... {BingoComp.teamdata.MVP:str}")


@bot.command()
async def woodcutxp(ctx: discord.ext.commands.Context):
	teamName = "special people"
	skill = "woodcutting"
	BingoComp = WOM.WOMcomp(WOMid)
	BingoComp.getData(skill)
	BingoComp.getTeamData(BingoComp.DataTeamLists, teamName)
	print("{BingoComp.teamdata.teamName:str} asked {skill:str} xp")
	await ctx.send("The {skill:str} xp of {BingoComp.teamdata.teamName:str} is ... {BingoComp.teamdata.TotalXP:str}")

@bot.command()
async def boardData(ctx: discord.ext.commands.Context):
	board = Bingo.BingoBoardOld()
	board.setCompletedTileTrue(2,3)
	board.setCompletedTileTrue(0,0)
	board.setCompletedTileTrue(4,4)
	board.setCompletedTileTrue(3,1)
	await board.fillBoard(ctx)

@bot.command()
async def w(ctx: discord.ext.commands.Context):
	message = await ctx.send("Do you love me?")
	await message.add_reaction('✅')
	await message.add_reaction('🏴󠁧󠁢󠁳󠁣󠁴󠁿')

@bot.command()
async def q(ctx: discord.ext.commands.Context):
	for descr in Bingo.bingoDescriptions:
		await ctx.send(descr)

@bot.command()
async def p(ctx: discord.ext.commands.Context):
	if ctx.author.id == 145345772995477504:
		await ctx.channel.purge()
	else:
		await ctx.channel.send(f'{ctx.author.name} stop')

@bot.command()
async def xxmakeTiles(ctx: discord.ext.commands.Context):
	if ctx.author.id == 145345772995477504:
		for x in Bingo.secretTilesjson:
			match x['type']:
				case "evidence":
					await ctx.send(x['description'])
				case "subtile evidence":
					for y in x['type specific']['subtiles']:

						await ctx.send(y['description'])
				case "subtile set evidence":
					for y in x['type specific']['subtileset']:
						for z in y['subtiles']: 
							await ctx.send(z['description'])
				case "count":
					print("count")
				case "set count":
					print("set count")
				case "xp":
					print("xp")
		
	else:
		await ctx.channel.send(f'{ctx.author.name} stop')




@bot.command()
async def makeBoard(ctx: discord.ext.commands.Context):
	team = "testTeam"
	Bingo.createBingoBoard(team)
	await ctx.send("board created")

@bot.command()
async def loadBoard(ctx: discord.ext.commands.Context):
	team = "testTeam"
	Bingo.createBingoBoard(team)
	await ctx.send("board created")


logging.basicConfig(level=logging.DEBUG)

bot.run(gTOKEN)    
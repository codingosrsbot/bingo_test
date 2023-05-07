
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
 
with open("./config/WOM.txt", 'r') as fp:
    WOMid = fp.readline().rstrip('\n')
    WOMgid = fp.readline().rstrip('\n')

with open("./config/tiles.json", 'r') as f:
    Bingotilesjson = json.load(f)


# Bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True

description = '''Discord osrs bot'''
bot = commands.Bot(intents=intents, command_prefix= "<" , description='Bingo time',  case_insensitive=True)

WOMg = WOM.WOMGroup(WOMgid)
	

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    myIntervalTasks.start()
    
@bot.event
async def on_reaction_add(reaction, user):
	if reaction.message.content == 'Do you love me?' and str(reaction.emoji) == '✅'and user != reaction.message.author:
		channel = reaction.message.channel
		role = discord.utils.get(user.roles, name='bingo admin')
		if role is not None:
			await channel.send(f'{user.name} loves me! aaaaaaaaaaaaaaaa <3')
		else:
			await channel.send(f'{user.name} is icky! waaaaaaaaaaa')
	if reaction.message.content == 'Do you love me?' and str(reaction.emoji) == '🏴󠁧󠁢󠁳󠁣󠁴󠁿'and user.id == 145345772995477504:
		await channel.send(f'{user.name} is the best')
    
@tasks.loop(seconds=3600)
async def myIntervalTasks():
	print("WOM gorup updating")
	#WOMg.updateGroup()
 

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
	BingoComp.getData(skill)
	BingoComp.getTeamData(BingoComp.DataTeamLists, teamName)
	print(BingoComp.teamdata.teamName + " asked " + skill +" mvp")
	await ctx.send("The " + skill  + " mvp of " + BingoComp.teamdata.teamName + " is ... " + BingoComp.teamdata.MVP)


@bot.command()
async def woodcutxp(ctx: discord.ext.commands.Context):
	id = 24073
	teamName = "special people"
	skill = "woodcutting"
	BingoComp = WOM.WOMcomp(WOMid)
	BingoComp.getData(skill)
	BingoComp.getTeamData(BingoComp.DataTeamLists, teamName)
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
async def w(ctx: discord.ext.commands.Context):
	message = await ctx.send("Do you love me?")
	await message.add_reaction('✅')
	await message.add_reaction('🏴󠁧󠁢󠁳󠁣󠁴󠁿')

@bot.command()
async def q(ctx: discord.ext.commands.Context):
	for x in Bingotilesjson:
		message = await ctx.send(x['description'])
		await message.add_reaction('✅')
		await message.add_reaction('🏴󠁧󠁢󠁳󠁣󠁴󠁿')

@bot.command()
async def p(ctx: discord.ext.commands.Context):
	await ctx.channel.purge()


logging.basicConfig(level=logging.DEBUG)

bot.run(gTOKEN)
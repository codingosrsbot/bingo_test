
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
 
with open("./config/WOM.json", 'r') as f:
    WOMjson = json.load(f)
    WOMid = WOMjson['competition id']
    WOMgid = WOMjson['group id']
    
with open("./config/Bingoadmins.json", 'r') as f:
    Bingoadminjson = json.load(f)
    BingoAdminRole = Bingoadminjson['admin role']
    BingoOrganizerid = Bingoadminjson['organizer id']

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
	channel = reaction.message.channel
	for x in Bingotilesjson:
		if reaction.message.content == str(x['description']) and str(reaction.emoji) == '✅'and user != reaction.message.author:
			role = discord.utils.get(user.roles, rname= str(BingoAdminRole))
			if role is not None:
				await channel.send(f"{user.name} approved {x['description']}")
			else:
				await channel.send(f'{user.name} you are not an admin!')
		else:
			if reaction.message.content == str(x['description']) and str(reaction.emoji) == '🏴󠁧󠁢󠁳󠁣󠁴󠁿':
				channel = reaction.message.channel
				ownerGuild = bot.guilds[0]  # Get the first guild the bot is a member of
				ownerUser = discord.utils.get(ownerGuild.members, id=BingoOrganizerid)
				if user.id == ownerUser.id:
					await channel.send(f'{ownerUser.name} is the best')
				else: 
					await channel.send(f'{user.name} stop pretending to be {ownerUser.name}')
			else:
				channel = reaction.message.channel
				print(x['description'])
				print(str(reaction.emoji))
				await channel.send(f'{user.name} this did not work')
    
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
	if discord.utils.get(ctx.author.roles, name=str(BingoAdminRole)) is not None:
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
	if ctx.author.id == 145345772995477504:
		await ctx.channel.purge()
	else:
		await ctx.channel.send(f'{ctx.author.name} stop')


logging.basicConfig(level=logging.DEBUG)

bot.run(gTOKEN)
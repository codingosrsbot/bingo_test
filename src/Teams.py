import discord #pip install discord.py
from discord.ext import commands
import asyncio
import logging
import os.path
import json


dictionary = {
    "name": "",
    "Members": 56,
    "Field": 8.6,
    "WatchList": "yes"
    }


def InitTeam(NameTeam):
    """Create Json file and init startup values"""
    dictionary["name"] = str(NameTeam)
    json_object = json.dumps(dictionary, indent=4)
    f = open(f"TeamsData/{NameTeam}.txt", "x")
    f.write(json_object)

async def printdict(ctx, NameTeam):
    with open(f"TeamsData/{NameTeam}.txt", 'r') as openfile:
        json_object = json.load(openfile)
        await ctx.send(json_object)
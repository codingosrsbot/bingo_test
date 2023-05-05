from PIL import Image #pip install pillow
from io import BytesIO
import discord #pip install discord.py
from discord.ext import commands

async def fillBoard(ctx):
	boardsize = (1428,2000)
	completesize = (200,200)
	tilesize = (286,232)
	boardstartpoint = (0,600)

	backgound = Image.open('board.png')
	overlay = Image.open('complete.png')
	overlay = overlay.resize(completesize)
	board = backgound.copy()

	rows = 5
	cols = 5
	i = 0
	for i in range(rows):
		for j in range(cols):
			board.paste(overlay, (43+(i*286),610+(j*232)), overlay)
	bytes = BytesIO()
	board.save(bytes, format="PNG")
	bytes.seek(0)
	dBoard = discord.File(bytes, filename="board.png")

	await ctx.send("your board", file=dBoard)
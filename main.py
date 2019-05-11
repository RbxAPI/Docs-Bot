import discord
from discord.ext import commands
import os
from utils import *

description = "Roblox API Server Documentation Bot"
bot = commands.Bot(command_prefix='?',description=description)
repo_list = Auto.get_repo_list()

@bot.event
async def on_ready():
	print("Logged in as "+str(bot.user.name)+", id: "+str(bot.user.id))
	print("--")

@bot.command()
async def list(ctx):
	print(repo_list)
	embed = discord.Embed(title="Roblox API - Library List",description="General library list specific to this server",color=0xFFFFFF)
	for repo in repo_list:
		embed.add_field(name=repo_list[repo]["name"],value=repo_list[repo]["link"],inline=False)
	await ctx.send(embed=embed)



if __name__ == "__main__":
	bot.run("Token")
import os
import traceback

import discord
from discord.ext import commands

from dotenv import load_dotenv
load_dotenv()

# A list containing all cogs that we want to load
available_cogs = ['cogs.maintenance', 'cogs.logging', 'cogs.utility', 'cogs.channels', 'cogs.moderation',
                  'cogs.verification', 'cogs.tagging']

# Bot Init
description = "Roblox API Server Documentation Bot"
bot = commands.Bot(command_prefix='?', description=description, help_command=None)

# Client Login
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}, id: {bot.user.id}")
    print("--")

# Event Error
@bot.event
async def on_error(event, *args, **kwargs):
    channel = channel = bot.get_channel(770843267327721502)
    emb = discord.Embed(color=discord.Color.red())
    emb.set_author(name="Error (Event)", icon_url="https://cdn.discordapp.com/attachments/336577284322623499/683028692133216300/ac6e275e1f638f4e19af408d8440e1d1.png")
    emb.add_field(name="Event", value=event, inline=False)
    emb.add_field(name="Traceback", value=traceback.format_exc(), inline=False)
    await channel.send(embed=emb)

# Command Error
@bot.event
async def on_command_error(ctx, error):
    channel = channel = bot.get_channel(770843267327721502)
    emb = discord.Embed(color=discord.Color.red())
    emb.set_author(name="Error (Commands)", icon_url="https://cdn.discordapp.com/attachments/336577284322623499/683028692133216300/ac6e275e1f638f4e19af408d8440e1d1.png")
    emb.add_field(name="Error", value=error, inline=False)
    emb.add_field(name="Command", value=ctx.command, inline=False)
    emb.add_field(name="Message", value=ctx.message.content, inline=False)
    await channel.send(embed=emb)

if __name__ == '__main__':

    # Load Cogs in list
    for cog in available_cogs:
        bot.load_extension(cog)

    # Run Bot
    bot.run(os.getenv("DISCORD_TOKEN"))

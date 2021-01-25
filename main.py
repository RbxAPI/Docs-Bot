import os
import traceback

import discord
from discord.ext import commands

from dotenv import load_dotenv

from cogs.moderation import default_embed

load_dotenv()

# A list containing all cogs that we want to load
available_cogs = ['cogs.maintenance', 'cogs.logging', 'cogs.utility', 'cogs.channels', 'cogs.moderation',
                  'cogs.tagging']

# Disabled Cogs
# 'cogs.verification'

# Bot Init
description = "Roblox API Server Documentation Bot"
intent = discord.Intents.default()
intent.members = True
bot = commands.Bot(command_prefix='?', description=description, help_command=None)


# Client Login
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}, id: {bot.user.id}")
    print("--")


# Event Error. the args are required
@bot.event
async def on_error(event, *args, **kwargs):
    channel = bot.get_channel(int(os.getenv('ERROR_LOGS_CHANNEL')))
    emb = default_embed('Error (Event)', color=discord.Color.red())
    emb.add_field(name="Event", value=event, inline=False)
    emb.add_field(name="Traceback", value=traceback.format_exc(), inline=False)
    await channel.send(embed=emb)


# Command Error
@bot.event
async def on_command_error(ctx, error):
    channel = bot.get_channel(int(os.getenv('ERROR_LOGS_CHANNEL')))
    emb = default_embed('Error (Commands)', color=discord.Color.red())
    emb.add_field(name="Error", value=error, inline=False)
    emb.add_field(name="Command", value=ctx.command, inline=False)
    emb.add_field(name="Message", value=ctx.message.content, inline=False)
    await channel.send(embed=emb)


if __name__ == '__main__':
    async def prep():
        await bot.wait_until_ready()
        # Load Cogs in list
        for cog in available_cogs:
            bot.load_extension(cog)

    # Run Bot
    bot.loop.create_task(prep())
    bot.run(os.getenv("DISCORD_TOKEN"))

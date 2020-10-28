import os
import traceback

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
    await channel.send(f'**Events**\nEvent: {event}\nTraceback: {traceback.format_exc()}')

# Command Error
@bot.event
async def on_command_error(message, error):
    channel = channel = bot.get_channel(770843267327721502)
    await channel.send(f'**Commands**\nError: {error}\nMessage: {message}\n')

if __name__ == '__main__':

    # Load Cogs in list
    for cog in available_cogs:
        bot.load_extension(cog)

    # Run Bot
    bot.run(os.getenv("DISCORD_TOKEN"))

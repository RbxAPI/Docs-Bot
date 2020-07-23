import os

from discord.ext import commands

from dotenv import load_dotenv
load_dotenv()

# A list containing all cogs that we want to load
available_cogs = ['cogs.maintenance', 'cogs.logging', 'cogs.utility', 'cogs.channels', 'cogs.moderation',
                  'cogs.verification', 'cogs.tagging']

# Bot Init
description = "Roblox API Server Documentation Bot"
bot = commands.Bot(command_prefix='?', description=description, help_command=None)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}, id: {bot.user.id}")
    print("--")


if __name__ == '__main__':

    # Load Cogs in list
    for cog in available_cogs:
        bot.load_extension(cog)

    # Run Bot
    bot.run(os.getenv("DISCORD_TOKEN"))

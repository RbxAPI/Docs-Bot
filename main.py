import discord
from discord.ext import commands

import docstoken
from utils import *

import requests
import json

description = "Roblox API Server Documentation Bot"
bot = commands.Bot(command_prefix='?', description=description)
bot.remove_command("help")
repo_list = Auto.get_repo_list()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}, id: {bot.user.id}")
    print("--")
    activity = discord.Activity(
        name="noobs",
        type=discord.ActivityType.watching
    )
    await bot.change_presence(activity=activity)


@bot.event
async def on_command(ctx):
    m = f"{ctx.message.content} ::: @{ctx.message.author.name}({ctx.message.author.id}) #{ctx.channel.name}({ctx.channel.id}) [{ctx.guild.name}]({ctx.guild.id})"
    print(m)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.send(str(error))
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        x = ctx.invoked_with if ctx.invoked_subcommand is None else ctx.invoked_subcommand
        misarg = f"Missing argument:`{error.param.name}`. Check ``{bot.command_prefix}help {x}``!"
        await ctx.send(misarg)
    elif isinstance(error, discord.errors.Forbidden):
        pass
    else:
        await ctx.send("An unknown error occured.")
        raise error


@bot.command(aliases=["libs", "libraries", "librarylist"])
async def list(ctx):
    """Generate server library list"""
    embed = discord.Embed(title="Roblox API - Library List", description="General library list specific to this server",
                          color=0xFFFFFF)
    for repo in repo_list:
        embed.add_field(name=repo_list[repo]["name"], value=repo_list[repo]["link"], inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def ping(ctx):
    resp = await ctx.send('Pong! Loading...', delete_after=1.0)
    latensnap = bot.latency
    diff = resp.created_at - ctx.message.created_at
    totalms = 1000 * diff.total_seconds()
    emb = discord.Embed()
    emb.title = "Pong!"
    emb.add_field(name="Message δtime", value=f"{totalms}ms")
    emb.add_field(name="Bot websocket latency", value=f"{(1000 * latensnap):.1f}ms")
    await ctx.send(embed=emb)


@bot.command(aliases=["codeblocks"])
async def codeblock(ctx):
    emb = discord.Embed()
    emb.title = "No codeblock no help from libdevs kthx"
    emb.description = "Codeblock is a syntax highlighting feature from Markdown that allows us to send source codes " \
                      "that can be " \
                      "read easily. Because Discord's messages support Markdown, we can use codeblocks in Discord too."
    emb.add_field(name="How to use codeblock?", value="https://help.github.com/en/articles/creating-and-highlighting"
                                                      "-code-blocks#syntax-highlighting")
    await ctx.send(embed=emb)


@bot.command()
async def robloxdocs(ctx, doc: str, version: str):
    url = f'https://{doc}.roblox.com/docs/json/{version}'
    r = requests.get(url)
    data = json.loads(r.text)
    embed = discord.Embed(title=data['info']['title'])
    for name, value in data['paths'].items():
        method = [*value.items()][0][0]
        roblox = value[method]
        embed_value = roblox['summary'] + ' ' + method + '\n\n**Parameters**\n'
        for parameter in roblox['parameters']:
            embed_value += parameter['name'] + ': ' + parameter.get('description') or 'No description' + '\n'
        embed.add_field(name=method.upper() + ' ' + name, value=embed_value, inline=True)
    await ctx.send(embed=embed)


@bot.command(aliases=["apisites", "robloxapi"])
async def api(ctx):
    emb = discord.Embed()
    emb.colour = discord.Colour.from_rgb(255, 255, 255)
    emb.title = "Roblox API Site List"
    emb.description = "https://devforum.roblox.com/t/list-of-all-roblox-api-sites/154714/2"
    emb.add_field(name="BTRoblox API list",
                  value="https://github.com/AntiBoomz/BTRoblox/blob/master/README.md#api-docs")
    await ctx.send(embed=emb)


@bot.command()
async def resources(ctx):
    emb = discord.Embed()
    emb.colour = discord.Colour.from_rgb(255, 255, 255)
    emb.title = 'Useful Resources'
    emb.description = "Below is a list of useful resources for multiple programming languages."
    emb.add_field(name='Lua',
                  value='Learning Lua - http://www.lua.org/pil/contents.html \nRoblox Developer Hub - '
                        'https://www.robloxdev.com/resources \nRoblox API Reference - '
                        'https://www.robloxdev.com/api-reference')
    emb.add_field(name='JavaScript',
                  value='Learning Javascript - https://www.codecademy.com/learn/learn-javascript \nJavascript Intro - '
                        'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Introduction')
    emb.add_field(name='Python',
                  value='Learning Python - https://www.codecademy.com/learn/learn-python \nPython Intro - '
                        'https://wiki.python.org/moin/BeginnersGuide')
    emb.add_field(name='Java',
                  value='Learning Java - https://www.codecademy.com/learn/learn-java \nJava Intro - '
                        'https://docs.oracle.com/javase/tutorial/')
    await ctx.send(embed=emb)


if __name__ == "__main__":
    bot.run(docstoken.discord)

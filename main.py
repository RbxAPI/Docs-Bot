import discord
import requests
from discord.ext import commands
from discord.utils import get

import docstoken
import json

description = "Roblox API Server Documentation Bot"
bot = commands.Bot(command_prefix='?', description=description, help_command=None)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}, id: {bot.user.id}")
    print("--")


@bot.event
async def on_command(ctx):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        m = f"“DM-{ctx.message.id}”{ctx.message.content} ::: @{ctx.author.name}({ctx.author.id})"
    else:
        m = f"“Text-{ctx.message.id}”{ctx.message.content} ::: @{ctx.author.name}({ctx.author.id}) {ctx.channel.name}({ctx.channel.id}) [{ctx.guild.name}]({ctx.guild.id})"
    print(m)

@bot.command(aliases=["libs", "libraries", "librarylist"])
async def list(ctx):
    """Generate server library list"""
    embed = discord.Embed(title="Roblox API", description="General library list specific to this server")
    response = requests.get("https://raw.githubusercontent.com/RbxAPI/Docs-Bot/rewrite/api_list.json",headers={"Cache-Control": "no-cache"})
    data = json.loads(response.content)
    for language in data:
        for libraryName in data[language]:
            embed.add_field(name=libraryName, value=data[language][libraryName])
    await ctx.send(embed=embed)


@bot.command()
async def ping(ctx):
    resp = await ctx.send('Pong! Loading...', delete_after=1.0)
    diff = resp.created_at - ctx.message.created_at
    totalms = 1000 * diff.total_seconds()
    emb = discord.Embed()
    emb.title = "Pong!"
    emb.add_field(name="Message time", value=f"{totalms}ms")
    emb.add_field(name="API latency", value=f"{(1000 * bot.latency):.1f}ms")
    await ctx.send(embed=emb)


@bot.command(aliases=["codeblocks"])
async def codeblock(ctx):
    emb = discord.Embed()
    emb.title = "Codeblocks"
    emb.description = "Codeblock is a syntax highlighting feature from Markdown that allows us to send source codes that can be read easily. Because Discord's messages support Markdown, we can use codeblocks in Discord too."
    emb.add_field(name="How to use codeblock?", value="https://help.github.com/en/articles/creating-and-highlighting-code-blocks#syntax-highlighting")
    await ctx.send(embed=emb)


async def check_doc_exists(ctx, doc, version):
    url = f'https://{doc}.roblox.com/docs/json/{version}'
    r = requests.get(url)
    if r.status_code != 200:
        return await ctx.send("Sorry, those docs don't exist.")
    data = r.json()
    embed = discord.Embed(title=data['info']['title'], description=f'https://{doc}.roblox.com')
    return data, embed


@bot.command()
async def docs(ctx, doc: str, version: str):
    data, embed = await check_doc_exists(ctx, doc, version)
    i = 0
    for path in data['paths']:
        for method in data['paths'][path]:
            docs = data['paths'][path][method]
            desc = f"""{docs['summary']}"""
            embed.add_field(name=f"{method.upper()} {path}", value=desc, inline=True)
            if i >= 25:
                await ctx.send(embed=embed)
                embed = discord.Embed(title=data['info']['title'])
                i = 0
            i += 1
    await ctx.send(embed=embed)


@bot.command()
async def doc(ctx, doc: str, version: str, *args):
    keyword = ' '.join(args)
    data, embed = await check_doc_exists(ctx, doc, version)
    for path in data['paths']:
        for method in data['paths'][path]:
            docs = data['paths'][path][method]
            if docs['summary'].find(keyword) != -1:
                desc = f"""{docs['summary']}"""
                embed.add_field(name=f"{method.upper()} {path}", value=desc, inline=True)
                await ctx.send(embed=embed)
                return
    await ctx.send("Sorry, that keyword was not found in docs specified")


@bot.command()
async def leaderboard(ctx):
    roles = []
    for role in ctx.guild.roles:
        if role.name.endswith("news"):
            roles.append({
                "name": role.name,
                "count": len(role.members)
            })
    roles.sort(key=lambda x: x['count'], reverse=True)
    embed = discord.Embed(title="Subscriber leaderboards")
    for i in range(len(roles)):
        embed.add_field(name=f"{i+1}. {roles[i]['name']}", value=f"**Subscribers:** {roles[i]['count']}")
    await ctx.send(embed=embed)


@bot.command(aliases=["apisites", "robloxapi", "references", "reference"])
async def api(ctx):
    emb = discord.Embed()
    emb.title = "Roblox API - Reference List"
    emb.description = "https://api.roblox.com/docs?useConsolidatedPage=true"
    emb.add_field(name="BTRoblox API list",
                  value="https://github.com/AntiBoomz/BTRoblox/blob/master/README.md#api-docs")
    emb.add_field(name="Robloxapi Github IO list",
                  value="https://robloxapi.github.io/ref/index.html , https://robloxapi.github.io/ref/updates.html")
    emb.add_field(name="Devforum list", value="https://devforum.roblox.com/t/list-of-all-roblox-api-sites/154714/2")
    emb.add_field(name="Deprecated Endpoints list",
                  value="https://devforum.roblox.com/t/official-list-of-deprecated-web-endpoints/62889")
    await ctx.send(embed=emb)


@bot.command()
async def resources(ctx):
    emb = discord.Embed()
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


@bot.command(pass_context=True)
async def subscribe(ctx):
    emoji_subscribe = '👍'
    emoji_unsubscribe = '👎'
    channelName = ctx.message.channel.name
    author = ctx.message.author
    roles = ctx.message.guild.roles
    message = ctx.message

    # Get the actual role
    hasRole = get(author.roles, name=channelName[channelName.find("_") + 1:] + " news")
    role = get(roles, name=channelName[channelName.find("_") + 1:] + " news")

    # If user has role, unsubscribe to channel
    if hasRole is not None:
        await author.remove_roles(hasRole)
        await message.add_reaction(emoji_unsubscribe)

    # if user doesn't have role, subscribe to channel
    if role is not None and hasRole is None:
        await author.add_roles(role)
        await message.add_reaction(emoji_subscribe)


@bot.command(pass_context=True)
@commands.has_role("Library Developer")
async def pingnews(ctx, version: str, *args):
    message = ' '.join(args)
    channelName = ctx.message.channel.name
    author = ctx.message.author
    roles = ctx.message.guild.roles
    role = get(roles, name=channelName[channelName.find("_") + 1:] + " news")
    await role.edit(mentionable=True)

    # If role exists for that channel, ping it
    if role is not None:
        await ctx.send(f'{role.mention}\n**Release Notes {version}**\n{message}')
        await role.edit(mentionable=False)


@bot.command(pass_context=True)
@commands.has_role("Moderator")
async def pinglibrarydevelopers(ctx, *args):
    title = ' '.join(args[0:2])
    message = ' '.join(args[2:])
    roles = ctx.message.guild.roles
    role = get(roles, name="Library Developer")
    await role.edit(mentionable=True)

    # If role exists for that channel, ping it
    if role is not None:
        await ctx.send(f'{role.mention}\n**{title}**\n{message}')
        await role.edit(mentionable=False)


@bot.command(pass_context=True)
@commands.has_role("Moderator")
async def restart(ctx):
    await ctx.bot.logout()


# Disabled for now    
# bot.load_extension('verify')

if __name__ == "__main__":
    bot.run(docstoken.discord)

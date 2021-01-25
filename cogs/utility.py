import discord
from discord.ext import commands
import yaml
import aiohttp

from EmbedFactory import default_embed

session = aiohttp.ClientSession()


async def check_doc_exists(ctx, doc, version):
    base = f'https://{doc}.roblox.com'
    async with session.get(f'{base}/docs/json/{version}') as r:
        # throws ClientConnectException if base is not a valid subdomain e.g. xx.roblox.com
        if r.status != 200:
            await ctx.send("Sorry, those docs don't exist.")
            return
        else:
            data = await r.json()
            return data, discord.Embed(description=base)


async def fetch_embed(filename: str, author: str):
    with open(f'yaml/{filename}.yml') as file:
        j = file.read()
    d = yaml.load(j, Loader=yaml.FullLoader)
    emb = discord.Embed.from_dict(d)
    emb.set_author(name=author, icon_url='https://avatars1.githubusercontent.com/u/42101452?s=200&v=4')
    return emb, d


class Utility(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        resp = await ctx.send('Pong! Loading...', delete_after=1.0)
        diff = resp.created_at - ctx.message.created_at
        totalms = 1000 * diff.total_seconds()
        emb = default_embed('Pong!')
        emb.add_field(name="Message response time", value=f"{totalms}ms")  # Time for receive+process+reply cmd
        emb.add_field(name="API latency", value=f"{(1000 * self.bot.latency):.1f}ms")  # Official heartbeat latency
        await ctx.send(embed=emb)

    @commands.command(aliases=["libs", "libraries", "librarylist"])
    async def list(self, ctx):
        embed, yml = await fetch_embed('libs', 'Libraries')
        for lang in yml["list"]:
            for lib in lang['libs']:
                # It can only get users that have mutual servers  with the bot
                # use fetch_user() if want to fetch users that don't have mutual servers
                user = self.bot.get_user(lib["uid"])
                embed.add_field(name=f'{lib["name"]}({lang["lang"]})',
                                value=f'{lib["author"]}({user.mention}) - {lib["url"]}')
        await ctx.send(embed=embed)

    @commands.command(aliases=["codeblocks"])
    async def codeblock(self, ctx):
        emb, _ = await fetch_embed('codeblock', 'Codeblocks')
        await ctx.send(embed=emb)

    @commands.command(aliases=["cookies"])
    async def cookie(self, ctx):
        emb, _ = await fetch_embed('cookie', 'Cookies')
        await ctx.send(embed=emb)

    @commands.command()
    async def docs(self, ctx, doc: str, version: str):
        data, embed = await check_doc_exists(ctx, doc, version)
        if embed is None:
            return
        i = 0
        embed.set_author(name=f'{doc.capitalize()} {version}',
                         icon_url="https://avatars1.githubusercontent.com/u/42101452?s=200&v=4")
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

    @commands.command()
    async def doc(self, ctx, doc: str, version: str, *, args):
        data, embed = await check_doc_exists(ctx, doc, version)
        if embed is None:
            return
        embed.set_author(name=f'{doc.capitalize()} {version}',
                         icon_url="https://avatars1.githubusercontent.com/u/42101452?s=200&v=4")
        embed.set_footer(text=f'Keyword(s): {args}')
        for path in data['paths']:
            for method in data['paths'][path]:
                docs = data['paths'][path][method]
                if docs['summary'].find(args) != -1:
                    desc = f"""{docs['summary']}"""
                    embed.add_field(name=f"{method.upper()} {path}", value=desc, inline=True)
                    await ctx.send(embed=embed)
                    return
        await ctx.send("Sorry, that keyword was not found in docs specified")

    @commands.command(aliases=["apisites", "robloxapi", "references", "reference"])
    async def api(self, ctx):
        emb, _ = await fetch_embed('endpoints', 'References')
        await ctx.send(embed=emb)

    @commands.command()
    async def resources(self, ctx):
        emb, _ = await fetch_embed('resources', 'Resources')
        await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(Utility(bot))

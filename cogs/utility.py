import discord
from discord.ext import commands
import yaml
import aiohttp

session = aiohttp.ClientSession()


class Utility(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def fetch_embed(self, filename: str):
        with open(f'yaml/{filename}.yml') as file:
            j = file.read()
        d = yaml.load(j, Loader=yaml.FullLoader)
        return discord.Embed.from_dict(d), d

    async def check_doc_exists(self, ctx, doc, version):
        base = f'https://{doc}.roblox.com'
        async with session.get(f'{base}/docs/json/{version}') as r:
            if r.status != 200:
                return await ctx.send("Sorry, those docs don't exist."), None
            else:
                data = await r.json()
                return data, discord.Embed(description=base)

    @commands.command()
    async def ping(self, ctx):
        resp = await ctx.send('Pong! Loading...', delete_after=1.0)
        diff = resp.created_at - ctx.message.created_at
        totalms = 1000 * diff.total_seconds()
        emb = discord.Embed()
        emb.set_author(name="Pong!",
                       icon_url="https://cdn.discordapp.com/attachments/336577284322623499/683028692133216300/ac6e275e1f638f4e19af408d8440e1d1.png")
        emb.add_field(name="Message time", value=f"{totalms}ms")
        emb.add_field(name="API latency", value=f"{(1000 * self.bot.latency):.1f}ms")
        await ctx.send(embed=emb)

    @commands.command(aliases=["libs", "libraries", "librarylist"])
    async def list(self, ctx):
        embed, yml = await self.fetch_embed('libs')
        embed.set_author(name="Libraries",
                         icon_url="https://cdn.discordapp.com/attachments/336577284322623499/683028692133216300/ac6e275e1f638f4e19af408d8440e1d1.png")
        for lang in yml["list"]:
            for lib in lang['libs']:
                # It can only get users that have mutual servers  with the bot
                # use fetch_user() if want to fetch users that don't have mutual servers
                user = self.bot.get_user(lib["uid"])
                embed.add_field(name=f'{lib["name"]}({lang["lang"]})', value=f'{lib["author"]}(@{user}) - {lib["url"]}')
        await ctx.send(embed=embed)

    @commands.command(aliases=["codeblocks"])
    async def codeblock(self, ctx):
        emb, _ = await self.fetch_embed('codeblock')
        emb.set_author(name="Codeblocks",
                       icon_url="https://cdn.discordapp.com/attachments/336577284322623499/683028692133216300/ac6e275e1f638f4e19af408d8440e1d1.png")
        await ctx.send(embed=emb)

    @commands.command(aliases=["cookies"])
    async def cookie(self, ctx):
        emb, _ = await self.fetch_embed('cookie')
        emb.set_author(name="Cookies",
                       icon_url="https://cdn.discordapp.com/attachments/336577284322623499/683028692133216300/ac6e275e1f638f4e19af408d8440e1d1.png")
        await ctx.send(embed=emb)

    @commands.command()
    async def docs(self, ctx, doc: str, version: str):
        data, embed = await self.check_doc_exists(ctx, doc, version)
        if embed is None:
            return
        i = 0
        embed.set_author(name=f'{doc.capitalize()} {version}',
                         icon_url="https://cdn.discordapp.com/attachments/336577284322623499/683028692133216300/ac6e275e1f638f4e19af408d8440e1d1.png")
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
        data, embed = await self.check_doc_exists(ctx, doc, version)
        if embed is None:
            return
        embed.set_author(name=f'{doc.capitalize()} {version}',
                         icon_url="https://cdn.discordapp.com/attachments/336577284322623499/683028692133216300/ac6e275e1f638f4e19af408d8440e1d1.png")
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
        emb, _ = await self.fetch_embed('endpoints')
        emb.set_author(name="References",
                       icon_url="https://cdn.discordapp.com/attachments/336577284322623499/683028692133216300/ac6e275e1f638f4e19af408d8440e1d1.png")
        await ctx.send(embed=emb)

    @commands.command()
    async def resources(self, ctx):
        emb, _ = await self.fetch_embed('resources')
        emb.set_author(name="Resources",
                       icon_url="https://cdn.discordapp.com/attachments/336577284322623499/683028692133216300/ac6e275e1f638f4e19af408d8440e1d1.png")
        await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(Utility(bot))

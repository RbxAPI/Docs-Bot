import discord, random, aiohttp
from discord.ext import commands

class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.words = ['apple', 'pie', 'cheese', 'dog', 'cat', 'sanjay', 'pancake', 'bloxy cola', 'bloxy is bad', 'node.js is bad', 'python is good.']
        self.client = aiohttp.ClientSession()

    async def UsernameById(self, user):
        url = f'https://api.roblox.com/users/{user}'
        r = await self.client.get(url)
        r = await r.json()
        return r.get('Id')

    @commands.command()
    async def verify(self, ctx):
        url = f'https://verify.eryn.io/api/user/{ctx.message.author.id}'
        r = await self.client.get(url)
        r = await r.json()
        if r['status'] == 'ok':
            username = await self.UsernameById(r['robloxId'])
            await ctx.message.member.edit(nick=username)
            await ctx.message.member.add_roles(336577687529193472)
        else:
            pass
            #not in eryn db

    @commands.Cog.listener()
    async def on_member_join(self, member):
        url = f'https://verify.eryn.io/api/user/{member.id}'
        r = await self.client.get(url)
        r = await r.json()
        if r['status'] == 'ok':
            username = await self.UsernameById(r['robloxId'])
            await member.edit(nick=username)
            await member.add_roles(336577687529193472)
        else:
            pass
            #not in eryn db

def setup(bot):
    bot.add_cog(Verify(bot))

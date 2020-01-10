import discord, random, aiohttp
from discord.ext import commands


class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.words = ['apple', 'pie', 'cheese', 'dog', 'cat', 'sanjay', 'pancake', 'bloxy cola', 'bloxy is bad',
                      'node.js is bad', 'python is good.']
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
            await ctx.author.edit(nick=username)
            await ctx.author.add_roles(336577687529193472)
            embed = discord.Embed(
                title='User Verified',
                description=f'{ctx.author.mention} has been verified as {username}',
                color=0x008e00
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send(
                f'{ctx.author.mention} :exclamation::wave: You must be new! Please go to '
                f'https://verify.eryn.io/ and follow the instructions on the page in order to get verified.')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        url = f'https://verify.eryn.io/api/user/{member.id}'
        r = await self.client.get(url)
        r = await r.json()
        if r['status'] == 'ok':
            username = await self.UsernameById(r['robloxId'])
            await member.edit(nick=username)
            await member.add_roles(336577687529193472)
            embed = discord.Embed(
                title='User Verified',
                description=f'{member.mention} has been verified as {username}',
                color=0x008e00
            )
            await member.guild.get_channel(335789594236813313).send(embed=embed)
        else:
            pass
            # not in eryn db


def setup(bot):
    bot.add_cog(Verify(bot))

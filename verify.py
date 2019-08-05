import discord, random, aiohttp
from discord.ext import commands

class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.words = ['apple', 'pie', 'cheese', 'dog', 'cat', 'sanjay', 'pancake', 'bloxy cola', 'bloxy is bad', 'node.js is bad', 'python is good.']
        self.client = aiohttp.ClientSession()

    async def IdByUsername(self, user):
        url = f'https://api.roblox.com/users/get-by-username?username={user}'
        r = await self.client.get(url)
        r = await r.json()
        return r.get('Id')

    async def get_status(self, id):
        url = f'https://www.roblox.com/users/profile/profileheader-json?userId={id}'
        r = await self.client.get(url)
        r = await r.json()
        return r.get('UserStatus')

    @commands.command()
    async def verify(self, ctx, user: str):
        roblox_id = await self.IdByUsername(user)
        if not roblox_id:
            return await ctx.send(':x: We could not find that user on roblox')
        code = f'{random.choice(self.words)} {random.choice(self.words)} {random.choice(self.words)} {random.choice(self.words)} {random.choice(self.words)} {random.choice(self.words)}'
        await ctx.send(f'Please put `{code}` as your **ROBLOX** status, and then say done')
        await self.bot.wait_for('message', check=lambda m: m.author.id == ctx.author.id and m.channel.id == ctx.channel.id and m.content == 'done', timeout=300)
        status = await self.get_status(roblox_id)
        if status == code:
            await ctx.send(f'✅ You have been verified as `{user}`')
            #add role
            #add to db
        else:
            await ctx.send(':x: I was unable to find the code on your profile.')



def setup(bot):
    bot.add_cog(Verify(bot))

import os
import discord
from discord.ext import commands
from discord import utils
import discord.emoji

class Channels(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def get_news_role(self, ctx, channel: discord.TextChannel = None):
        ch = channel if channel else ctx.channel
        return utils.find(lambda r: r.name.startswith(ch.name.split('_')[1]), ctx.guild.roles)
    
    @commands.command()
    async def leaderboard(self, ctx):
        roles = [(r.name, len(r.members)) for r in ctx.guild.roles if 'news' in r.name]
        roles.sort(key=lambda x: x[1], reverse=True)
        embed = discord.Embed()
        embed.set_author(name="Subscriber Leaderboards", icon_url="https://cdn.discordapp.com/attachments/336577284322623499/683028692133216300/ac6e275e1f638f4e19af408d8440e1d1.png")
        for i, r in enumerate(roles):
            embed.add_field(name=f"{i + 1}. {r[0]}", value=f"**Subscribers:** {r[1]}")
        await ctx.send(embed=embed)
    
    @commands.command()
    async def subscribe(self, ctx, channel: discord.TextChannel = None):

        # bot_commands channel
        if ctx.channel.id == os.getenv("BOT_COMMANDS_CHANNEL") and channel:
            role = self.get_news_role(ctx, channel)
        
        # Not bot_commands channel, but is a channel in "Libraries" or "Frameworks" categories
        elif (ctx.channel.id != os.getenv("BOT_COMMANDS_CHANNEL") or ctx.channel.category_id == os.getenv("LIBRARIES_CATEGORY") or ctx.channel.category_id == os.getenv("FRAMEWORKS_CATEGORY")) and not channel:
            role = self.get_news_role(ctx)
        else:
            return

        if role in ctx.author.roles:
            await ctx.author.remove_roles(role)
            await ctx.message.add_reaction('👎')
        else:
            await ctx.author.add_roles(role)
            await ctx.message.add_reaction('👍')
    
    @commands.command()
    @commands.has_role("Library Developer")
    async def poll(self, ctx, *, args):
        role = self.get_news_role(ctx)
        await role.edit(mentionable=True)
        await ctx.send(f'{role.mention}')
        await role.edit(mentionable=False)
        embed = discord.Embed(Title="Poll")
        embed.set_author(name="Poll", icon_url="https://cdn.discordapp.com/attachments/336577284322623499/683028692133216300/ac6e275e1f638f4e19af408d8440e1d1.png")
        hasEmojis = ((args.find('[') and args.find(']')) != -1) # Regex?

        if hasEmojis:
            emojis = (args[args.find('[')+1:args.find(']')-1]).split()
            args = args[args.find(']')+1:]
            embed.add_field(name="Question", value=f'{args}')
            embed.set_footer(text='React below to cast a vote')
            message = await ctx.send(embed=embed)
            for _emoji in emojis:
                await message.add_reaction(_emoji)
        else:
            embed.add_field(name="Question", value=f'{args}')
            embed.set_footer(text="👍 for upvote or 👎 for downvote")
            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')
            await message.add_reaction('👎')
    
    @commands.command()
    @commands.has_role("Library Developer")
    async def pingnews(self, ctx, version: str, *, args):
        role = self.get_news_role(ctx)
        await role.edit(mentionable=True)
        await ctx.send(f'{role.mention}\n**Release Notes {version}**\n{args}')
        await role.edit(mentionable=False)
    
def setup(bot):
    bot.add_cog(Channels(bot))
import discord
from discord.ext import commands
from discord import utils
import discord.emoji
from .data import Data

db = Data() # Initialize database

class Tagging(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def tag(self, ctx, name: str):
        result = db.taggingEntry.fetch(name, ctx.message.channel.id)
        if result == None:
            await ctx.send(f'Tag with identifier "{name}" does not exist.')
            return
        emb = discord.Embed()
        emb.set_footer(text=f'\t\t\t\t\t\t\tTimestamp: {result["date"]}', icon_url="https://cdn.discordapp.com/attachments/336577284322623499/683028692133216300/ac6e275e1f638f4e19af408d8440e1d1.png")
        emb.add_field(name=f'{name}', value=result["content"], inline=False)
        await ctx.send(embed=emb)
    
    @commands.command()
    async def tag_list(self, ctx):
        result = db.taggingEntry.fetchAll(ctx.message.channel.id)
        if len(result) == 0:
            await ctx.send(f'Tags in this channel "<#{ctx.message.channel.id}>" does not exist.')
            return
        emb = discord.Embed()
        #emb.set_footer(text=f'\t\t\t\t\t\t\tTimestamp: {result["date"]}', icon_url="https://cdn.discordapp.com/attachments/336577284322623499/683028692133216300/ac6e275e1f638f4e19af408d8440e1d1.png")
        for entry in result:
            emb.add_field(name=f'{entry["index"]}', value=f';{entry["name"]}', inline=False)

        await ctx.send(embed=emb)

    
    @commands.command()
    @commands.has_role("Library Developer")
    async def tag_add(self, ctx, name, *, content: str):
        result = db.taggingEntry.check_indentifier(name)

        # If Tag already exists, prevent duplicates
        if result:
            await ctx.send(f'Tag "{name}" already exists.')
            return

        db.taggingEntry.insert(ctx.message.channel.id, name, content, ctx.message.created_at)
        await ctx.send(f'Tag "{name}" created.')
    
    @commands.command()
    @commands.has_role("Library Developer")
    async def tag_index(self, ctx, name: str):
        result = db.taggingEntry.fetch(name, ctx.message.channel.id)
        if result == None:
            await ctx.send(f'Tag with identifier "{name}" does not exist.')
            return
        await ctx.send(f'Tag with identifier "{name}" has an index of "{result["index"]}"')
    
    @commands.command()
    @commands.has_role("Library Developer")
    async def tag_edit(self, ctx, id, *, newContent: str):
        result = db.taggingEntry.update(id, content=newContent, date=ctx.message.created_at)
        if result:
            await ctx.send(f'Tag index of "{id}" updated successfully.')
            return
        await ctx.send(f'Tag index of "{id}" failed to update.')

def setup(bot):
    bot.add_cog(Tagging(bot))
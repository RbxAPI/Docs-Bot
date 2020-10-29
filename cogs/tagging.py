import discord
import discord.emoji
from discord.ext import commands

from .data import Data

db = Data()  # Initialize database


class Tagging(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def tag(self, ctx, name=None):
        if name:
            result = db.taggingEntry.fetch(name, ctx.message.channel.id)
            if result is None:
                await ctx.send(f'Tag with identifier "{name}" does not exist.')
                return
            emb = discord.Embed()
            emb.set_footer(text=f'\t\t\t\t\t\t\tTimestamp: {result["date"]}',
                           icon_url="https://cdn.discordapp.com/attachments/336577284322623499/683028692133216300/ac6e275e1f638f4e19af408d8440e1d1.png")
            emb.add_field(name=f'{name}', value=result["content"], inline=False)
            await ctx.send(embed=emb)
        else:
            result = db.taggingEntry.fetch_all(ctx.message.channel.id)
            i = 0
            if len(result) == 0:
                await ctx.send(f'Tags in this channel "<#{ctx.message.channel.id}>" does not exist.')
                return
            emb = discord.Embed(title="Available tags for channel")
            for entry in result:
                emb.add_field(name=f'Tag', value=f'({i}:{entry["index"]}) ?tag {entry["name"]}', inline=False)
                i += 1
            await ctx.send(embed=emb)

    @tag.command()
    @commands.has_role("Library Developer")
    async def add(self, ctx, name, *, content: str):
        result = db.taggingEntry.fetch(name, ctx.message.channel.id)

        # If Tag already exists, prevent duplicates
        if result:
            await ctx.send(f'Tag "{name}" already exists.')
            return

        db.taggingEntry.insert(ctx.message.channel.id, name, content, ctx.message.created_at)
        await ctx.send(f'Tag "{name}" created.')

    @tag.command()
    @commands.has_role("Library Developer")
    async def index(self, ctx, name: str):
        result = db.taggingEntry.fetch(name, ctx.message.channel.id)
        if result:
            await ctx.send(f'Tag with identifier "{name}" has an index of "{result["index"]}"')
            return
        await ctx.send(f'Tag with identifier "{name}" does not exist.')

    @tag.command()
    @commands.has_role("Library Developer")
    async def edit(self, ctx, id, *, newContent: str):
        result = db.taggingEntry.update(id, content=newContent, date=ctx.message.created_at)
        if result:
            await ctx.send(f'Tag index of "{id}" updated successfully.')
            return
        await ctx.send(f'Tag index of "{id}" failed to update.')


def setup(bot):
    bot.add_cog(Tagging(bot))

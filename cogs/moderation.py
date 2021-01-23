import os

import discord
from discord import utils
from discord.ext import commands

from .data import Data

db = Data()  # Initialize database


def process_action(ctx, title, emb, member: discord.Member, msg, duration=None):
    emb.add_field(name=title, value=f'{member.mention} ({member.id})', inline=False)
    if duration:
        emb.add_field(name='Duration', value=f'{duration}', inline=False)
    emb.add_field(name="Reason", value=f'{msg}', inline=False)
    emb.add_field(name="Moderator",
                  value=ctx.message.author.mention,
                  inline=False)
    # Add data to database
    # (Action, Duration, Reason, Moderator, Target, Date)
    db.modEntry.insert(title, duration, msg, ctx.message.author.id, member.id,
                       ctx.message.created_at)


def prepare_action(ctx, name: str):
    role = utils.get(ctx.guild.roles, name=name)
    # Create default embed
    emb = discord.Embed()
    emb.set_author(name="Moderation",
                   icon_url="https://cdn.discordapp.com/attachments/336577284322623499/683028692133216300/ac6e275e1f638f4e19af408d8440e1d1.png")
    emb.set_footer(text=f'\t\t\t\t\t\t\tTimestamp: {ctx.message.created_at}')
    channel = ctx.message.channel
    return role, emb, channel


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.log_ch = None  # moderation-logs channel

    @commands.Cog.listener()
    async def on_ready(self):
        self.log_ch = self.bot.get_channel(int(os.getenv("MODERATION_LOGS_CHANNEL")))

    @commands.command()
    @commands.has_role("Moderator")
    async def ping_library_developers(self, ctx, title, *, message):
        role = utils.get(ctx.guild.roles, name="Library Developer")
        await role.edit(mentionable=True)
        await ctx.send(f'{role.mention}\n**{title}**\n{message}')
        await role.edit(mentionable=False)

    @commands.command()
    @commands.has_any_role("Library Developer", "Moderator")
    async def mute(self, ctx, member: discord.Member, duration, *, message):
        role, emb, channel = prepare_action(ctx, 'Muted')

        # If Moderator invokes, mute from server and not just channel
        if utils.get(ctx.guild.roles, name='Moderator') in ctx.message.author.roles:
            process_action(ctx, 'Mute (Server)', emb, member, message, duration)
            await member.add_roles(role)

        # If Library Developer invokes, mute from channel and not server
        if ((utils.get(ctx.guild.roles, name="Library Developer") in ctx.message.author.roles) and (
                channel.category.name == "libraries" or channel.category.name == "frameworks")):
            process_action(ctx, 'Mute (Channel)', emb, member, 'n/a', None)
            await channel.set_permissions(member, read_messages=True, send_messages=False)

        await ctx.message.add_reaction('👍')
        await self.log_ch.send(embed=emb)

    @commands.command()
    @commands.has_any_role("Library Developer", "Moderator")
    async def unmute(self, ctx, member: discord.Member, *, message):
        role, emb, channel = prepare_action(ctx, 'Muted')

        # If Moderator invokes, unmute from server and not just channel
        if utils.get(ctx.guild.roles, name="Moderator") in ctx.message.author.roles:
            process_action(ctx, 'Unmute (Server)', emb, member, message, None)
            await member.remove_roles(role)

        # If Library Developer invokes, unmute from channel and not server
        elif ((utils.get(ctx.guild.roles, name="Library Developer") in ctx.message.author.roles) and (
                channel.category.name == "libraries" or channel.category.name == "frameworks")):
            process_action(ctx, 'Unmute (Channel)', emb, member, message, None)
            await channel.set_permissions(member, overwrite=None)

        await ctx.message.add_reaction('👍')
        await self.log_ch.send(embed=emb)

    @commands.command()
    @commands.has_role("Moderator")
    async def warn(self, ctx, member: discord.Member, *, message):
        _, emb, channel = prepare_action(ctx, '')
        process_action(ctx, 'Warn', emb, member, message, None)

        await ctx.message.add_reaction('👍')
        await self.log_ch.send(embed=emb)

    @commands.command()
    @commands.has_role("Moderator")
    async def infractions(self, ctx, member: discord.Member):
        i = 0

        # Fetch data from database
        query = db.modEntry.fetch(member.id)

        # If no data exists for user, abort
        if len(query) == 0:
            await ctx.send(f'User "{member.id}" has no infractions.')
            return

        _, emb, _ = prepare_action(ctx, '')

        for case in query:
            emb.add_field(name=f'Case Number: {case["index"]}',
                          value=f'Action: {case["action"]}\nDuration: {case["duration"]}\nUser: {case["target"]}\n'
                                f'Reason: {case["reason"]}\nModerator: {case["moderator"]}\n Date: {case["date"]}',
                          inline=False)
            if i >= 25:
                await ctx.send(embed=emb)
                i = 0
            i += 1
        await ctx.send(embed=emb)

    @commands.command()
    @commands.has_role("Moderator")
    async def reason(self, ctx, id, *, message):
        sent = db.modEntry.update(id, reason=message)
        if sent:
            await ctx.send(f'Case Number "{id}" was updated successfully.')
            return
        await ctx.send(f'Case Number "{id}" failed to update.')

    @commands.command()
    @commands.has_role("Moderator")
    async def duration(self, ctx, id, *, _duration):
        sent = db.modEntry.update(id, _duration=_duration)
        if sent:
            await ctx.send(f'Case Number "{id}" was updated successfully.')
            return
        await ctx.send(f'Case Number "{id}" failed to update.')

    @commands.command()
    @commands.has_role("Moderator")
    async def clean(self, ctx, amount: int, member: discord.Member = None):
        _, emb, ch = prepare_action(ctx, '')
        emb.add_field(name='Message (Clean)', value=ch.mention, inline=False)
        emb.add_field(name="Moderator", value=ctx.message.author.mention, inline=False)

        if member:
            emb.insert_field_at(1, name="From", value=member.mention, inline=False)

            def is_member(message):
                return message.author.id == member.id

            msgs = await ctx.message.channel.purge(limit=amount+1, check=is_member)
            amount = len(msgs) - 1
        # If specific member is not specified
        else:
            await ctx.message.channel.purge(limit=amount+1)
        emb.insert_field_at(1, name="Amount", value=str(amount), inline=False)
        await self.log_ch.send(embed=emb)


def setup(bot):
    bot.add_cog(Moderation(bot))

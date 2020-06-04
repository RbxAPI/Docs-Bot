import discord
from discord.ext import commands
from discord import utils

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role("Moderator")
    async def restart(self, ctx):
        await self.bot.logout()

    @commands.command()
    @commands.has_role("Moderator")
    async def pinglibrarydevelopers(self, ctx, title, *, message):
        role = utils.get(ctx.guild.roles, name="Library Developer")
        await role.edit(mentionable=True)
        await ctx.send(f'{role.mention}\n**{title}**\n{message}')
        await role.edit(mentionable=False)
    
    @commands.command()
    @commands.has_role("Library Developer" or "Moderator")
    async def mute(self, ctx, member: discord.Member, duration, *, message):
        role = utils.get(ctx.guild.roles, name="Muted")
        channel = ctx.message.channel
        log_channel = self.bot.get_channel(709262930750865440) # moderation-logs channel

        # Create default embed
        entries = await ctx.message.guild.audit_logs(limit=None, action=discord.AuditLogAction.channel_update).flatten()
        base_entry = entries[0]

        emb = discord.Embed()
        emb.set_author(name="Moderation", icon_url="https://cdn.discordapp.com/attachments/336577284322623499/683028692133216300/ac6e275e1f638f4e19af408d8440e1d1.png")
        emb.set_footer(text=f'\t\t\t\t\t\t\tTimestamp: {ctx.message.created_at}')

        # If Moderator invokes, mute from server and not just channel
        if ((utils.get(ctx.guild.roles, name="Moderator") in ctx.message.author.roles)):
            emb.add_field(name="Mute (Server)", value=f'{member.mention} ({member.id})', inline=False)
            emb.add_field(name="Duration", value=f'n/a', inline=False)
            emb.add_field(name="Reason", value=f'n/a', inline=False)
            emb.add_field(name="Moderator", value=f'{ctx.message.author}#{ctx.message.author.discriminator} ({ctx.message.author.id})', inline=False)
            await member.add_roles(role)

            # Add data to database
            # (Action, Duration, Reason, Moderator)


        # If Library Developer invokes, mute from channel and not server
        elif ((utils.get(ctx.guild.roles, name="Library Developer") in ctx.message.author.roles) and (channel.category.name == "libraries" or channel.category.name == "frameworks")):
            emb.add_field(name="Mute (Channel)", value=f'{member.mention} ({member.id})', inline=False)
            emb.add_field(name="Duration", value=f'n/a', inline=False)
            emb.add_field(name="Reason", value=f'n/a', inline=False)
            emb.add_field(name="Moderator", value=f'{ctx.message.author}#{ctx.message.author.discriminator} ({ctx.message.author.id})', inline=False)
            await channel.set_permissions(member, read_messages=True, send_messages=False)

            # Add data to database
            # (Action, Duration, Reason, Moderator)
        
        await ctx.message.add_reaction('👍')
        await log_channel.send(embed=emb)
    
    @commands.command()
    @commands.has_role("Library Developer" or "Moderator")
    async def unmute(self, ctx, member: discord.Member, *, message):
        role = utils.get(ctx.guild.roles, name="Muted")
        channel = ctx.message.channel
        log_channel = self.bot.get_channel(709262930750865440) # moderation-logs channel

        # Create default embed
        entries = await ctx.message.guild.audit_logs(limit=None, action=discord.AuditLogAction.channel_update).flatten()
        base_entry = entries[0]

        emb = discord.Embed()
        emb.set_author(name="Moderation", icon_url="https://cdn.discordapp.com/attachments/336577284322623499/683028692133216300/ac6e275e1f638f4e19af408d8440e1d1.png")
        emb.set_footer(text=f'\t\t\t\t\t\t\tTimestamp: {ctx.message.created_at}')

        # If Moderator invokes, unmute from server and not just channel
        if ((utils.get(ctx.guild.roles, name="Moderator") in ctx.message.author.roles)):
            emb.add_field(name="Unmute (Server)", value=f'{member.mention} ({member.id})', inline=False)
            emb.add_field(name="Duration", value=f'n/a', inline=False)
            emb.add_field(name="Reason", value=f'n/a', inline=False)
            emb.add_field(name="Moderator", value=f'{ctx.message.author}#{ctx.message.author.discriminator} ({ctx.message.author.id})', inline=False)
            await member.remove_roles(role)

            # Add data to database
            # (Action, Duration, Reason, Moderator)

        # If Library Developer invokes, unmute from channel and not server
        elif ((utils.get(ctx.guild.roles, name="Library Developer") in ctx.message.author.roles) and (channel.category.name == "libraries" or channel.category.name == "frameworks")):
            emb.add_field(name="Unmute (Channel)", value=f'{member.mention} ({member.id})', inline=False)
            emb.add_field(name="Reason", value=f'n/a', inline=False)
            emb.add_field(name="Moderator", value=f'{ctx.message.author}#{ctx.message.author.discriminator} ({ctx.message.author.id})', inline=False)
            await channel.set_permissions(member, overwrite=None)

            # Add data to json
            # (Action, Duration, Reason, Moderator)
        
        await ctx.message.add_reaction('👍')
        await log_channel.send(embed=emb)

def setup(bot):
    bot.add_cog(Moderation(bot))
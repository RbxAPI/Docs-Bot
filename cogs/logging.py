import os
import discord
from discord.ext import commands

class Logging(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Message Logging
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        channel = self.bot.get_channel(int(os.getenv("MESSAGE_LOGS_CHANNEL"))) # message-logs channel

        # Avoid duplicate channel; i.e message delete from log channel
        if message.channel == channel:
            return
        
        # Check Audit logs to find out who deleted the message
        entries = await message.guild.audit_logs(limit=None, action=discord.AuditLogAction.message_delete).flatten()
        base_entry = entries[0]

        emb = discord.Embed()
        emb.set_author(name="Message (Delete)", icon_url="https://cdn.discordapp.com/attachments/336577284322623499/683028692133216300/ac6e275e1f638f4e19af408d8440e1d1.png")
        emb.set_footer(text=f'{message.author}\t\t\t\t\t\tTimestamp: {message.created_at}', icon_url=message.author.avatar_url)
        emb.add_field(name="Message", value=message.content)
        await channel.send(embed=emb)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        channel = self.bot.get_channel(int(os.getenv("MESSAGE_LOGS_CHANNEL"))) # message-logs channel
    
        # If message data is malformed or blank, return
        if (before.content == "") or (after.content == ""):
            return
        
        emb = discord.Embed()
        emb.set_author(name="Message (Edit)", icon_url="https://cdn.discordapp.com/attachments/336577284322623499/683028692133216300/ac6e275e1f638f4e19af408d8440e1d1.png")
        emb.set_footer(text=f'{before.author}\t\t\t\t\t\tTimestamp: {after.created_at}', icon_url=before.author.avatar_url)
        emb.add_field(name="Before", value=(before.content), inline=False)
        emb.add_field(name="After", value=(after.content), inline=False)
        await channel.send(embed=emb)

def setup(bot):
    bot.add_cog(Logging(bot))
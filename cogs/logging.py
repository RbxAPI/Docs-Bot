import os

from discord import TextChannel
from discord.ext import commands

from embed import footer_embed


class Logging(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.log_ch: TextChannel = self.bot.get_channel(int(os.getenv("MESSAGE_LOGS_CHANNEL")))

    # Message Logging
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        emb = footer_embed(message, 'Message (Delete)', message.author.avatar_url)

        # Avoid duplicate channel; i.e message delete from log channel
        if message.channel == self.log_ch:
            return

        emb.add_field(name="Message", value=message.content)
        await self.log_ch.send(embed=emb)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        # If message data is malformed or blank, return
        if (before.content == "") or (after.content == ""):
            return

        emb = footer_embed(after, 'Message (Edit)', before.author.avatar_url)
        emb.add_field(name="Before", value=before.content, inline=False)
        emb.add_field(name="After", value=after.content, inline=False)
        await self.log_ch.send(embed=emb)


def setup(bot):
    bot.add_cog(Logging(bot))

import os
import discord
from discord.ext import commands
from discord import utils
import requests
from .data import Data
import random
from datetime import datetime

db = Data()  # Initialize database

available_words = ["apple", "orange", "pear", "boat", "ship", "car", "plane", "train", "turtle", "cow", "frog",
                   "sheep"]  # Obstain from the number's 6 & 9 due to Roblox's filter
tempStorage = []  # Holds Random Keys


class Verification(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Verification on member join
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(int(os.getenv("JOIN_LOGS_CHANNEL")))  # join-logs channel
        role = utils.get(member.guild.roles, name="Verified")
        response = requests.get(f'https://verify.eryn.io/api/user/{member.id}').json()

        if response["status"] == "ok":
            # Change nickname (Error if attempting to change server owner's nickname)

            # Abort if already in database
            result = db.verificationEntry.check_discordid(member.id)
            if result:
                await member.edit(nick=response["robloxUsername"])
                await self.bot.add_roles(member, role)
                await member.add_roles(role)
                await channel.send(f'Verified "{member.mention}" as "{response["robloxUsername"]}" (current)')
                return
            db.verificationEntry.insert(member.id, response["robloxUsername"], response["robloxId"], datetime.now())
            await member.edit(nick=response["robloxUsername"])
            await member.add_roles(role)
            await channel.send(f'Verified "{member.mention}" as "{response["robloxUsername"]}" 4')
        else:
            channel_dm = await member.create_dm()
            await channel_dm.send(
                f'It appears that you are not verified with RoVer or our own database. A keyphrase has been sent to '
                f'your dms. Please verify w/ ``?verify`` in our server.')

    @commands.command()
    async def verify(self, ctx, username: str = None, *, keyPhrase: str = None):
        member = ctx.message.author
        role = utils.get(ctx.guild.roles, name="Verified")
        channel = self.bot.get_channel(int(os.getenv("JOIN_LOGS_CHANNEL")))  # join-logs channel
        response = requests.get(f'https://verify.eryn.io/api/user/{member.id}').json()

        result = db.verificationEntry.check_discordid(member.id)
        if result:
            await member.edit(nick=response["robloxUsername"])
            await member.add_roles(role)
            await channel.send(f'Verified "{member.mention}" as "{response["robloxUsername"]}" (current)')
            return

        # Blank Verify (RoVer-based Method)
        if username is None and keyPhrase is None:
            if response["status"] == "ok":

                # Change nickname (Error if attempting to change server owner's nickname)
                db.verificationEntry.insert(member.id, response["robloxUsername"], response["robloxId"],
                                            ctx.message.created_at)
                await ctx.message.author.edit(nick=response["robloxUsername"])
                await member.add_roles(role)
                await ctx.send(f'Successfully verified as "{response["robloxUsername"]}" 3')
                await channel.send(f'Verified "{member.mention}" as "{response["robloxUsername"]}" (current)')
            else:
                # User is not verified with RoVer Service; port to our own solution
                channel = await member.create_dm()
                temp_passphrase = ' '.join((random.choice(available_words) for i in range(8)))
                tempStorage.append({
                    "discord_id": member.id,
                    "pass_phrase": temp_passphrase
                })
                await channel.send(
                    f'Here is your passphrase to verify. Please place this string of text (without quotes) "{temp_passphrase}" in your roblox profile blurb.')
                await ctx.send(
                    f'It appears that you are not verified with RoVer or our own database. A keyphrase has been sent '
                    f'to your dms. Please reverify w/ ``?verify <username> <keyphrase>``')

        # Custom Verify (Custom solution)
        elif username and keyPhrase:
            userid = requests.get(f'https://api.roblox.com/users/get-by-username?&username={username}').json()["Id"]
            response_2 = requests.get(f'https://users.roblox.com/v1/users/{userid}/status').json()["status"]
            for temps in tempStorage:
                if temps["discord_id"] == member.id and temps["pass_phrase"] == response_2:
                    # Change nickname (Error if attempting to change server owner's nickname)
                    tempStorage.remove(temps)
                    db.verificationEntry.insert(member.id, username, userid, ctx.message.created_at)
                    await ctx.message.author.edit(nick=username)
                    await member.add_roles(role)
                    await ctx.send(f'Successfully verified as "{response_2["robloxUsername"]}" 2')
                    await channel.send(f'Verified "{member.mention}" as "{response_2["robloxUsername"]}" 5')
                    return
            await ctx.send(f'Failed to verify as "{username}"')

    @commands.command()
    async def info(self, ctx, member: discord.Member):

        # Fetch data from database
        query = db.verificationEntry.fetch(member.id)

        # If no data exists for user, abort
        if not query:
            await ctx.send(f'User "{member.id}" is not verified.')
            return

        emb = discord.Embed()
        emb.set_author(name="Information",
                       icon_url="https://cdn.discordapp.com/attachments/336577284322623499/683028692133216300/ac6e275e1f638f4e19af408d8440e1d1.png")
        emb.set_footer(text=f'\t\t\t\t\t\t\tTimestamp: {ctx.message.created_at}')
        emb.add_field(name=f'**{member.display_name}**',
                      value=f'Discord Id: {query["discordid"]}\nUsername: {query["username"]}\nUser Id: {query["userid"]}\nDate: {query["date"]}',
                      inline=False)
        emb.add_field(name=f'Profile', value=f'https://www.roblox.com/users/{query["userid"]}/profile', inline=False)
        await ctx.send(embed=emb)

    @commands.command()
    @commands.has_role("Moderator")
    async def force_verify(self, ctx, username, member: discord.Member):
        role = utils.get(ctx.guild.roles, name="Verified")
        userid = requests.get(f'https://api.roblox.com/users/get-by-username?&username={username}').json()["Id"]
        channel = self.bot.get_channel(int(os.getenv("JOIN_LOGS_CHANNEL")))  # join-logs channel

        # Prevent overwrite
        result = db.verificationEntry.check_discordid(member.id)
        if result:
            await member.edit(nick=username)
            await member.add_roles(role)
            await ctx.send(f'Successfully forced verified "{username}" as "{member.mention}" (current)')
            await channel.send(f'Successfully forced verified "{username}" as "{member.mention}" (current)')
            return

        db.verificationEntry.insert(member.id, username, userid, ctx.message.created_at)
        await member.edit(nick=username)
        await member.add_roles(role)
        await ctx.send(f'Successfully forced verified "{username}" as "{member.mention}" 1')
        await channel.send(f'Successfully forced verified "{username}" as "{member.mention}"')

    @commands.command()
    @commands.has_role("Moderator")
    async def verify_check(self, ctx, member: discord.Member):
        await ctx.send(db.verificationEntry.check_discordid(member.id))


def setup(bot):
    bot.add_cog(Verification(bot))

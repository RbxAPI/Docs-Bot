from discord.ext import commands


class Maintenance(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Maintenance Commands
    @commands.command(name='reload')
    @commands.has_role("Moderator")
    async def reload(self, ctx, *, name: str):
        try:
            self.bot.unload_extension(name)
            self.bot.load_extension(name)
        except Exception as error:
            await ctx.send(f'Error: {error}')
        else:
            await ctx.send(f'Reloaded: {name}')


def setup(bot):
    bot.add_cog(Maintenance(bot))

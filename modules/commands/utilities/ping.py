from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """Honestly every bot just needs this"""
        lang = self.bot.utils.LanguageHandler.get_language(self, guild_id=ctx.author.guild.id)
        await ctx.send(lang['ping_1'].format(str(round(self.bot.latency*1000))))


def setup(bot):
    bot.add_cog(Ping(bot))
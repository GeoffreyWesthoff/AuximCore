import discord
from discord.ext import commands

class Duck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def duck(self, ctx):
        """Gets you a picture of a duck"""
        lang = self.bot.utils.LanguageHandler.get_language(self, guild_id=ctx.author.guild.id)
        async with self.bot.web.get('https://random-d.uk/api/v1/quack') as r:
            response = await r.json()
            embed = discord.Embed(title=lang['duck_1'])
            embed.set_image(url=response['url'])
            embed.set_footer(text=response['message'])
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Duck(bot))


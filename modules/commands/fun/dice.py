import random
import discord
from discord.ext import commands


class Dice:
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(usage='<number>')
    async def dice(self, ctx, *, num: int):
        """Roll a dice"""
        lang = self.bot.utils.LanguageHandler.get_language(self, guild_id=ctx.author.guild.id)
        if num:
            number = random.randint(1, num)
            embed = discord.Embed(title=lang['dice_1'].format(str(num)), description=lang['dice_2'].format(str(number)))
            embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

    @dice.error
    async def no_arg(self, ctx, error):
        lang = self.bot.utils.LanguageHandler.get_language(self, guild_id=ctx.author.guild.id)
        if isinstance(error, commands.MissingRequiredArgument):
            num = 6
            number = random.randint(1, 6)
            embed = discord.Embed(title=lang['dice_1'].format(str(num)), description=lang['dice_2'].format(str(number)))
            await ctx.send(embed=embed)
        if isinstance(error, commands.BadArgument):
            await ctx.send(lang['dice_3'])


def setup(bot):
    bot.add_cog(Dice(bot))

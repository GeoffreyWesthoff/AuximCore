import discord
from discord.ext import commands
import sys


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def info(self, ctx):
        """Bot statistics and information"""
        lang = self.bot.utils.LanguageHandler.get_language(self, guild_id=ctx.author.guild.id)
        owner = await self.bot.application_info()
        em = discord.Embed(title=lang['info_1'])
        em.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        em.add_field(name=lang['info_2'], value='{}.{}.{}'.format(str(sys.version_info.major), str(sys.version_info.minor), str(sys.version_info.micro)))
        em.add_field(name=lang['info_3'], value=str(len(self.bot.guilds)))
        em.add_field(name=lang['info_4'], value=str(discord.__version__))
        em.add_field(name=lang['info_5'], value='{}/{} {}'.format(str(ctx.guild.shard_id), str(self.bot.shard_count), lang['info_6']))
        em.add_field(name=lang['info_7'], value=str(owner.owner))
        em.add_field(name=lang['info_8'], value=str(round(self.bot.latency*1000)) + 'ms')
        em.set_footer(text=lang['info_9'].format(self.bot.user.id))
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Info(bot))

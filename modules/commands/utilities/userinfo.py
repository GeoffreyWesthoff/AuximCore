import discord
from discord.ext import commands


class Userinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(usage='<member>')
    async def userinfo(self, ctx, *, member: discord.Member):
        """Userinfo command"""
        lang = self.bot.utils.LanguageHandler.get_language(self, guild_id=ctx.author.guild.id)
        em = discord.Embed(color=member.color)
        em.set_author(name=str(member), icon_url=member.avatar_url)
        em.set_thumbnail(url=member.avatar_url)
        em.add_field(name=lang['userinfo_1'], value=str(member.created_at.strftime('%a, %-d %b %Y {} %H:%M:%S GMT'.format(lang['userinfo_6']))))
        em.add_field(name=lang['userinfo_2'], value=str(member.joined_at.strftime('%a, %-d %b %Y {} %H:%M:%S GMT'.format(lang['userinfo_6']))))
        em.add_field(name=lang['userinfo_3'], value=str(member.status))
        if member.id == member.guild.owner.id:
            em.add_field(name=lang['userinfo_4'], value=lang['userinfo_5'])
        em.set_footer(text='ID: {}'.format(str(member.id)), icon_url=ctx.guild.icon_url)
        await ctx.send(embed=em)

    @userinfo.error
    async def error_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            lang = self.bot.utils.LanguageHandler.get_language(self, guild_id=ctx.author.guild.id)
            em = discord.Embed(color=ctx.author.color)
            member = ctx.author
            em.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
            em.set_thumbnail(url=ctx.author.avatar_url)
            em.add_field(name=lang['userinfo_1'], value=str(ctx.author.created_at.strftime('%a, %-d %b %Y {} %H:%M:%S GMT'.format(lang['userinfo_6']))))
            em.add_field(name=lang['userinfo_2'], value=str(ctx.author.joined_at.strftime('%a, %-d %b %Y {} %H:%M:%S GMT'.format(lang['userinfo_6']))))
            em.add_field(name=lang['userinfo_3'], value=str(member.status))
            if member.id == member.guild.owner.id:
                em.add_field(name=lang['userinfo_4'], value=lang['userinfo_5'])
            em.set_footer(text='ID: {}'.format(str(ctx.author.id)), icon_url=ctx.guild.icon_url)
            await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Userinfo(bot))

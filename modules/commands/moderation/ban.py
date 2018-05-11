import discord
from discord.ext import commands


class Ban:
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(usage='[member]')
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member,  *reason):
        """Bans a member"""
        lang = self.bot.utils.LanguageHandler.get_language(self, guild_id=ctx.guild.id)
        if ctx.author.top_role < member.top_role:
            return await ctx.send(lang['ban_3'])
        if reason:
            await member.ban(reason=str(reason))
            await ctx.send(str(member) + lang['ban_2'].format(str(reason[0])))
        else:
            await member.ban()
            await ctx.send(str(member) + lang['ban_1'])

    @ban.error
    async def handle_error(self, ctx, error):
        lang = self.bot.utils.LanguageHandler.get_language(self, guild_id=ctx.guild.id)
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(lang['ban_fail_1'])
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(lang['ban_fail_2'])
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send(lang['ban_fail_3'])


def setup(bot):
    bot.add_cog(Ban(bot))
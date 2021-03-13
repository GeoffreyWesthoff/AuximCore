import discord
from discord.ext import commands

class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(manage_guild=True)
    @commands.command(usage='[value]')
    async def settings(self, ctx, *, settings: int):
        """Change the bot's settings"""
        prefix = self.bot.utils.PrefixHelper.get_prefix(self.bot, ctx.message)
        language = self.bot.utils.LanguageHandler.get_language(self, guild_id=ctx.guild.id)
        current_lang = self.bot.utils.LanguageHandler.guild_lang(self, guild_id=ctx.guild.id)
        languages = self.bot.utils.LanguageHandler.list_languages(self)

        def check(msg):
            return msg.author.id == ctx.author.id and msg.channel == ctx.channel and (msg.content.lower() == 'yes' or msg.content.lower() == 'no')

        def check2(msg):
            return msg.author.id == ctx.author.id and msg.channel == ctx.channel

        def check3(msg):
            return msg.author.id == ctx.author.id and msg.channel == ctx.channel and msg.content.lower() in languages

        if settings == 1:
            await ctx.send(language['settings_1'].format(prefix))
            msg_1 = await self.bot.wait_for('message', check=check, timeout=60)
            if msg_1.content.lower() == 'yes':
                await ctx.send(language['settings_2'])
                msg_2 = await self.bot.wait_for('message', check=check2, timeout=60)
                self.bot.db.set(str(ctx.guild.id) + ':prefix', msg_2.content)
                await ctx.send(language['settings_3'].format(str(msg_2.content)))
            else:
                return await ctx.send(language['settings_7'])
        if settings == 2:
            langs = []
            for lang in languages:
                langs.append(lang + ', ')
            await ctx.send(language['settings_4'].format(current_lang.title()))
            msg_1 = await self.bot.wait_for('message', check=check, timeout=60)
            if msg_1.content.lower() == 'yes':
                await ctx.send(language['settings_5'].format(''.join(langs)))
                msg_2 = await self.bot.wait_for('message', check=check3, timeout=60)
                self.bot.db.set(str(ctx.guild.id) + ':language', msg_2.content)
                await ctx.send(language['settings_6'].format(str(msg_2.content)))
            else:
                return await ctx.send(language['settings_7'])

    @settings.error
    async def handle_error(self, ctx, error):
        prefix = self.bot.utils.PrefixHelper.get_prefix(self.bot, ctx.message)
        language = self.bot.utils.LanguageHandler.get_language(self, guild_id=ctx.guild.id)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(language['settings_8'].format(prefix))


def setup(bot):
    bot.add_cog(Settings(bot))

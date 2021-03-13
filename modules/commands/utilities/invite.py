import discord
from discord.ext import commands

class Invite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def invite(self, ctx):
        """Get the bots invite link"""
        perms = self.bot.utils.SettingsLoader.config['perms']
        await ctx.send('https://discordapp.com/oauth2/authorize?client_id={}&permissions={}&scope=bot'.format(str(self.bot.user.id), perms))

def setup(bot):
    bot.add_cog(Invite(bot))
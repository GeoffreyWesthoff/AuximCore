import discord
from discord.ext import commands
import json
import modules.utils as utils
import os

settings = json.load(open('settings.json'))
token = settings['token']
description = settings['description']
status = settings['status']


class Bot(commands.AutoShardedBot):
    """Subclassing Bot because we do some different things here"""
    @property
    def utils(self):
        """Define the default utilities"""
        return utils

    @property
    def web(self):
        """Makes aiohttp a global session"""
        return utils.WebHelper.session

    @property
    def db(self):
        """Makes Redis a global session"""
        return utils.DatabaseHandler.db

    async def on_ready(self):
        # Remove help because it's done with commands
        bot.remove_command('help')

        # Set status
        await self.change_presence(game=discord.Game(name=status))
        for file in os.listdir('modules/events'):
            # Load invisible cogs
            direc = 'modules.events.'
            if not file.startswith('__'):
                name = file.replace('.py','')
                self.load_extension(direc + name)
        for x in os.walk('modules/commands', topdown=False):
            # Load command cogs
            for y in x[1]:
                if not y.startswith('__'):
                    direc = 'modules.commands.{}.'.format(y)
                    for file in os.listdir('modules/commands/{}'.format(y)):
                        if not file.startswith('__'):
                            name = file.replace('.py','')
                            self.load_extension(direc + name)
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        print('All cogs loaded')
        print('------')
        print('Statistics')
        print(str(len(self.guilds)) + ' - ' + str(self.shard_count) + ' (Guilds/Shards)')
        print('------')
        print('Initialization Complete')


# Create a bot instance
bot = Bot(command_prefix=utils.PrefixHelper.get_prefix, description=description)


# Commands here will not show in the commands function


@bot.command()
@commands.is_owner()
async def load(ctx, extension_name : str):
    """Loads an extension."""
    try:
        bot.load_extension('modules.' + extension_name)
    except (AttributeError, ImportError) as e:
        await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await ctx.send("{} loaded.".format(extension_name))


@bot.command()
@commands.is_owner()
async def unload(ctx, extension_name : str):
    """Unloads an extension."""
    try:
        bot.unload_extension('modules.' + extension_name)
    except (AttributeError, ImportError) as e:
        await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await ctx.send("{} unloaded.".format(extension_name))


@bot.command()
@commands.is_owner()
async def reload(ctx, extension_name : str):
    """Reloads an extension."""
    try:
        bot.unload_extension('modules.' + extension_name)
        bot.load_extension('modules.' + extension_name)
    except (AttributeError, ImportError) as e:
        await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await ctx.send("{} reloaded.".format(extension_name))


@bot.command()
@commands.is_owner()
async def eval(ctx, *, code):
    """Eval's custom code"""
    try:
        result = exec(code)
        await ctx.send("```py\n{}```".format(result))
    except Exception as e:
        await ctx.send("```py\n{}```".format(e))


@bot.command()
async def commands(ctx):
    """Display the help function"""
    embed = discord.Embed(title='Help', description=bot.description)
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
    owner = await bot.application_info()
    embed.set_footer(text='Made by: ' + str(owner.owner))
    for x in os.walk('modules/commands', topdown=False):
        for y in x[1]:
            if not y.startswith('__'):
                commands_list = []
                for file in os.listdir('modules/commands/{}'.format(y)):
                    if not file.startswith('__'):
                        name = file.replace('.py', '')
                        command = bot.get_command(name)
                        if command is None:
                            continue
                        if command.usage is not None:
                            commands_list.append('**' + bot.command_prefix(bot, ctx.message) + command.name + ' ' + str(command.usage) + '**'+ '\n' + str(command.help) + '\n')
                        else:
                            commands_list.append('**' + bot.command_prefix(bot, ctx.message) + command.name + '**' + '\n' + str(command.help) + '\n')
                if commands_list != []:
                    embed.add_field(name='**' + y.title() + "**", value=''.join(commands_list))
    await ctx.send(embed=embed)

# Start the bot
bot.run(token)

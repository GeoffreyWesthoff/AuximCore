# AuximCore

## Requirements: 

* Redis
* discord.py rewrite

## Using AuximCore

Add your token to settings.json

Set your description, this will be filled in in the commands command.

Set your prefix, this is how you'll use the bot

Set your perms, this is used to generate the invite. Generate your permission code on the Discord Developers site

Set your status, this is your now playing status

If your bot is on DBL or BFD, set your API key, feel free to delete statposter.py if your bot is private

## Helpers

For web requests, use `self.bot.web` to use the global aiohttp connection
For the database, Redis, a simple kv storage is used. Use `self.bot.db` to access the Redis lib.

If you keep PrefixHelper and LanguageHandler,
this will automatically keep track of the language and prefix per server.

Some sample commands are included to assist you in creating your own commands and to see how helper functions are used.
Also provided in the utilities folder are meta commands that almost every bot has

## Commands

Commands follow the following structure.
`modules/commands/category/command.py`
Every command is expected to be a single file. Every command MUST have it's own file.

Events are cogs that are not exposed as commands, these work the same way as cogs, but are hidden from the user. They are put in:
`modules/events/event.py`

## Languages
To add a new language, simply copy the en.json file and rename it to your language. Please follow language naming conventions for ease of use.

Languages are automatically fetched with the LanguageHandler and are automatically found in the settings command


import redis
import aiohttp
import json
import asyncio
import os


class SettingsLoader:
    config = json.load(open('settings.json'))


class LanguageHandler:
    def get_language(self, guild_id):
        try:
            lang = DatabaseHandler.db.get(str(guild_id) + ":language").decode('utf-8')
            file = json.load(open('modules/languages/{}.json'.format(lang), encoding='utf-8'))
            return file
        except:
            return json.load(open('modules/languages/en.json', encoding='utf-8'))

    def list_languages(self):
        languages = []
        for file in os.listdir('modules/languages'):
            if file.endswith('.json'):
                languages.append(file.replace('.json',''))
        return languages

    def guild_lang(self, guild_id):
        try:
            lang = DatabaseHandler.db.get(str(guild_id) + ":language").decode('utf-8')
            return lang
        except:
            return 'en'


class PrefixHelper:
    def get_prefix(self, message):
        guild_id = message.guild.id
        try:
            prefix = DatabaseHandler.db.get(str(guild_id) + ':prefix').decode('utf-8')
        except AttributeError:
            prefix = SettingsLoader.config['prefix']
        return prefix


class DatabaseHandler:
    db = redis.Redis(db=10)


class WebHelper:
    session = aiohttp.ClientSession(loop=asyncio.get_event_loop())





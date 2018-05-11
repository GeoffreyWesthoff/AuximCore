from modules.utils import DatabaseHandler, SettingsLoader
import asyncio
import json


class StatPoster:
    def __init__(self, bot):
        self.bot = bot
        self.dbl_header = {'Authorization': SettingsLoader.config['dbl_key'], 'content-type': 'application/json'}
        self.bfd_header = {"Authorization": SettingsLoader.config['bfd_key'], "Content-Type": "application/json"}
        self.loop = bot.loop
        self.loop.create_task(self.poster())

    async def poster(self):
        while True:
            dbl_payload = {"server_count": len(self.bot.guilds), "shard_count": self.bot.shard_count}
            bfd_payload = {"server_count": len(self.bot.guilds)}
            DatabaseHandler.db.set('guild_count', value=str(len(self.bot.guilds)))
            async with self.bot.web.post('https://discordbots.org/api/bots/{}/stats'.format(str(self.bot.user.id)), headers=self.dbl_header, data=json.dumps(dbl_payload)) as dbl:
                response = await dbl.text()
                print('Guild count posted to DBL: [{}]: {}'.format(dbl.status, response))
            async with self.bot.web.post('https://botsfordiscord.com/api/v1/bots/{}'.format(str(self.bot.user.id)), headers=self.bfd_header, data=json.dumps(bfd_payload)) as bfd:
                response = await bfd.text()
                print('Guild count posted to BFD: [{}]: {}'.format(bfd.status, response))
            await asyncio.sleep(300)


def setup(bot):
    bot.add_cog(StatPoster(bot))

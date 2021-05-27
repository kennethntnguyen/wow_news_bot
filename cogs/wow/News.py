import discord
from discord.ext import commands, tasks
from logger import DatabaseLogger
from cogs.wow.wownewsdb import WoWNewsDB

import cogs.wow.config as cfg
import cogs.wow.messageembedder as me


class WoWNewsCog(commands.Cog, name='World of Warcraft News'):
    def __init__(self, bot: commands.Bot):
        self._bot = bot
        self._wow_news_db = WoWNewsDB()
        self._logger = DatabaseLogger(motor_client=self.wow_newsdb.client, database_name=cfg.mongodb_atlas['database_name'], collection_name=cfg.mongodb_atlas['log_collections']['commands'])

    @property
    def wow_newsdb(self):
        return self._wow_news_db

    @property
    def logger(self):
        return self._logger

    @commands.command()
    async def latest(self, ctx):
        """Shares the latest news for World of Warcraft"""
        article = await self.wow_newsdb.get_latest_regular_article()
        article = me.embed_message(title=article[cfg.article_keys['TITLE']], description=article[cfg.article_keys['DESCRIPTION']], url=article[cfg.article_keys['URL']], image_url=article[cfg.article_keys['IMAGE_URL']], datetime=article[cfg.article_keys['DATETIME']], color=cfg.news_cog['embed_color'], thumbnail=False)
        await ctx.send(embed=article)
        await self.log_command_usage(ctx)

    @commands.command(aliases=['hotfix','update','updates'])
    async def hotfixes(self, ctx):
        """Shares the latest hotfixes/updates for World of Warcraft"""
        article = await self.wow_newsdb.get_latest_hotfixes_article()
        article = me.embed_message(title=article[cfg.article_keys['TITLE']], description=article[cfg.article_keys['DESCRIPTION']], url=article[cfg.article_keys['URL']], image_url=article[cfg.article_keys['IMAGE_URL']], datetime=article[cfg.article_keys['DATETIME']], color=cfg.news_cog['embed_color'], thumbnail=False)
        await ctx.send(embed=article)
        await self.log_command_usage(ctx)


    def thumbnail(self, number_of_articles: int) -> bool:
        if number_of_articles == 1:
            return False
        else:
            return True

    async def log_command_usage(self, ctx):
        await self.logger.log_command(user_id=str(ctx.author), message=ctx.message.content, command=ctx.invoked_with)


class WoWNewsUpdaterCog(commands.Cog, name='World of Warcraft News Updater'):

    def __init__(self, bot: commands.Bot):
        self._bot = bot
        self._news_channel = bot.get_channel(cfg.updater_cog['news_channel_id'])
        self._wow_news_db = WoWNewsDB()
        self._logger = DatabaseLogger(motor_client=self.wow_newsdb.client, database_name=cfg.mongodb_atlas['database_name'], collection_name=cfg.mongodb_atlas['log_collections']['updater'])
        self._change_stream = None
        self._loop = bot.loop
        self.loop.create_task(self.news_change_stream())

    @property
    def loop(self):
        return self._loop

    @property
    def wow_newsdb(self):
        return self._wow_news_db

    @property
    def logger(self):
        return self._logger

    @property
    def news_channel(self):
        return self._news_channel

    @property
    def change_stream(self):
        return self._change_stream

    @change_stream.setter
    def change_stream(self, change_stream):
        self._change_stream = change_stream

    async def news_change_stream(self):
        pipeline = [
            {
                '$match': {
                    'operationType': 'update'
                }
            }
        ]
        async with self.wow_newsdb.news_collection.watch(pipeline=pipeline) as self.change_stream:
            await self.change_stream_send_message(self.change_stream)

    async def change_stream_send_message(self, changes):
        async for change in changes:
            try:
                update_fields = change['updateDescription']['updatedFields'].keys()
                if cfg.article_keys['TITLE'] in update_fields:
                    article = await self.wow_newsdb.get_article_by_id(change['documentKey']['_id'])
                    article = me.embed_message(title=article[cfg.article_keys['TITLE']], description=article[cfg.article_keys['DESCRIPTION']], url=article[cfg.article_keys['URL']], image_url=article[cfg.article_keys['IMAGE_URL']], datetime=article[cfg.article_keys['DATETIME']], color=cfg.news_cog['embed_color'], thumbnail=False)
                    await self.news_channel.send(embed=article)
            except Exception as e:
                print(e)

def setup(bot):
    bot.add_cog(WoWNewsCog(bot))
    print('World of Warcraft News Cog loaded...')
    bot.add_cog(WoWNewsUpdaterCog(bot))
    print('World of Warcraft News Updater Cog loaded...')

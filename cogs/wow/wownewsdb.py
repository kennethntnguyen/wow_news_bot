import datetime
import cogs.wow.config as cfg
from motor import motor_asyncio


class WoWNewsDB:
    def __init__(self):
        self._client = motor_asyncio.AsyncIOMotorClient(cfg.mongodb_atlas['connection_string'])
        self._database = self.client[cfg.mongodb_atlas['database_name']]
        self._news_collection = self.database[cfg.mongodb_atlas['news_collection_name']]
        self._change_stream = None

    async def has_id(self, article_id: list):
        return await self._news_collection.find_one({cfg.article_keys['ID']: article_id})

    @property
    def client(self):
        return self._client

    @property
    def database(self):
        return self._database

    @property
    def news_collection(self):
        return self._news_collection

    # Returns the latest Hotfixes/Update article
    @property
    async def hotfixes(self):
        return await self.get_latest_hotfixes_article()

    # Returns the latest article that is not a Hotfixes/Update article
    @property
    async def regular(self):
        return await self.get_latest_regular_article()

    # Returns the latest article that can either be a Hotfixes/Update or Regular article
    @property
    async def latest(self):
        return await self.get_latest_article()

    # Returns the latest article regardless of article type (Hotfixes/Update or Regular)
    async def get_latest_article(self):
        try:
            articles = self.news_collection.aggregate([
                {
                    '$sort': {cfg.article_keys['DATETIME']: -1}
                },
                {
                    '$limit': 1
                }
            ])
            if articles:
                article = await articles.to_list(length=None)
                if len(article) == 1:
                    return article.pop()
                else:
                    return None
            else:
                return None
        except Exception as e:
            print(
                'WoWNewsDB.get_latest: could not aggregate the latest WoW news article from database', e)

    # Returns the latest Non-Hotfixes/Update article
    async def get_article_by_id(self, id):
        try:
            article = await self.news_collection.find_one({cfg.article_keys['ID']: id})
            return article
        except Exception as e:
            print('WoWNewsDB.get_article_by_id: could not find WoW news article by id from database', e)

    # Returns the latest Non-Hotfixes/Update article
    async def get_latest_regular_article(self):
        try:
            article = await self.news_collection.find_one({cfg.article_keys['TYPE']: cfg.article_types['LATEST']})
            return article
        except Exception as e:
            print('WoWNewsDB.get_latest_non_hotfixes_article: could not find the latest non-hotfix WoW news article from database', e)

    # Returns the latest Hotfixes/Update
    async def get_latest_hotfixes_article(self):
        try:
            article = await self.news_collection.find_one({cfg.article_keys['TYPE']: cfg.article_types['HOTFIXES']})
            return article
        except Exception as e:
            print('WoWNewsDB.get_latest_hotfixes_article: could not find the latest WoW hotfixes article from database', e)

    # Return a list of database names
    async def list_database_names(self):
        return await self.client.list_database_names()

    # Return a list of collection names
    async def list_collection_names(self):
        return await self.database.list_collection_names()


class ArticlesNotFound(Exception):
    pass

class IncorrectType(Exception):
    pass
import os

mongodb_atlas = {
    "connection_string": os.environ.get('MONGODB_CONNECTION_STRING'),
    "database_name": "info-bot",
    "news_collection_name": "wow-news",
    "log_collections": {"commands": "user-commands-log", "updater": "push-updates-log"}
}

article_types = {
    "HOTFIXES": "hotfixes",
    "LATEST": "latest"
}

article_keys = {
    "TYPE": "type",
    "ID": "_id",
    "TITLE": "title",
    "DESCRIPTION": "description",
    "DATETIME": "datetime",
    "URL": "url",
    "IMAGE_URL": "image_url"
}

news_cog = {
    "embed_color": {
      "r": 252,
      "g": 186,
      "b": 3
    }
}

updater_cog = {
    "news_channel_id": 823082892367364156,
    "wow_role_id": 742188088461099148,
    "refresh_rate_seconds": 5,
    "embed_color": {
      "r": 255,
      "g": 75,
      "b": 35
    }
}

import datetime
import discord


def embed_message(title: str, description: str, url: str, image_url: str, datetime: datetime.datetime, color: dict, thumbnail: bool = True):
    embed = discord.Embed(title=title, description=description,
                          url=url, timestamp=datetime, color=discord.Color.from_rgb(r=color['r'], g=color['g'], b=color['b']), thumbnail=thumbnail)
    embed.set_thumbnail(
        url=image_url) if thumbnail else embed.set_image(url=image_url)
    return embed

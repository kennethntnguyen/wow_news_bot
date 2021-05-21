import discord
import wow_news_bot.config as cfg
from discord.ext import commands

class Help(commands.DefaultHelpCommand):
    def __init__(self):
        commands.DefaultHelpCommand.__init__(self, no_category='Other Commands')

bot = commands.Bot(command_prefix=cfg.command_prefix, case_insensitive=True, help_command=Help())

def user_is_admin(ctx):
    return ctx.message.author.id in cfg.administrator_ids

@bot.command(hidden=True)
@commands.check(user_is_admin)
async def load(ctx, extension):
    try:
        bot.load_extension(f'cogs.{extension}')
        await ctx.send(f'Extension **{extension}** successfully loaded')
    except commands.ExtensionAlreadyLoaded:
        await ctx.send(f'Extension **{extension}** is already loaded')
    except commands.ExtensionNotFound:
        await ctx.send(f'Extension **{extension}** does not exist')
    except (commands.NoEntryPointError, commands.ExtensionFailed):
        await ctx.send(f'Extension loading error')


@bot.command(hidden=True)
@commands.check(user_is_admin)
async def unload(ctx, extension):
    try:
        bot.unload_extension(f'cogs.{extension}')
        await ctx.send(f'Extension **{extension}** successfully unloaded')
    except commands.ExtensionNotLoaded:
        await ctx.send(f'Extension **{extension}** has not initially been loaded')


@bot.command(hidden=True)
@commands.check(user_is_admin)
async def reload(ctx, extension):
    try:
        bot.reload_extension(f'cogs.{extension}')
        await ctx.send(f'Extension **{extension}** successfully reloaded')
    except commands.ExtensionNotLoaded:
        await ctx.send(f'Extension **{extension}** has not initially been loaded')
    except commands.ExtensionNotFound:
        await ctx.send(f'Extension **{extension}** does not exist')
    except (commands.NoEntryPointError, commands.ExtensionFailed):
        await ctx.send(f'Extension loading error')


@bot.command()
@commands.check(user_is_admin)
async def stop(ctx):
    """Shuts down the Info Bot"""
    if user_is_admin(ctx):
        await ctx.send(f'**{ctx.author.name}#{ctx.author.discriminator}** stopped the Info bot.')
        await bot.logout()
    else:
        await ctx.send(f'**{ctx.author.name}#{ctx.author.discriminator}** does not have administrator rights.')


@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f'**{ctx.message.content}** is not a valid command.\n\nType **.help** command for more info on commands.\nYou can also type **.help *category*** or **.help *command*** for additional info.')
    print(error)


@bot.event
async def on_ready():
    print(
        f'Logged in as {bot.user.name}#{bot.user.discriminator} with user ID {bot.user.id}')
    bot.load_extension('info_bot.cogs.wow.News')
    print('Info Bot has started...')


bot.run(cfg.token)

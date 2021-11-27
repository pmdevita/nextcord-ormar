from nextcord.ext import commands
from tortoise import Tortoise
import argparse

DEFAULT_CONFIG = {
    "connections": None,
    "apps": None,
}

AERICH_APP = {
    "models": ["aerich.models"],
    "default_connection": "default",
}

APP_TEMPLATE = {
    "models": None,
    "default_connection": "default"
}


def cogs_to_apps(bot: commands.Bot):
    apps = {"aerich": AERICH_APP}
    for cog_name in bot.cogs:
        cog = bot.cogs[cog_name]
        class_ = cog.__class__
        module = class_.__module__

        app = APP_TEMPLATE.copy()
        app["models"] = [module]
        apps[cog_name] = app
    return apps


def bot_to_config(bot: commands.Bot, database_uri: str = None, config: dict = None):
    if config is None:
        config = DEFAULT_CONFIG.copy()
    if database_uri:
        if isinstance(config.get("connections", None), list):
            config["connections"].append({"default": database_uri})
        elif config.get("connections", None) is None:
            config["connections"] = {"default": database_uri}
    config["apps"] = cogs_to_apps(bot)
    return config


async def connect_tortoise(bot: commands.Bot, database_uri: str = None, config: dict = None):
    config = bot_to_config(bot, database_uri, config)
    await Tortoise.init(config)


def attach_argparse_group(parser: argparse.ArgumentParser):
    group = parser.add_argument_group("aerich")
    group.add_argument("--aerich")
    group.add_argument("--app")
    group.add_argument("--delete", action="store_true")

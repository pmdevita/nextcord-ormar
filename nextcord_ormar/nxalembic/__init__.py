import configparser
import os
import sys

import alembic.util.exc
from alembic.config import Config, command
from nextcord_ormar import Bot, OrmarManager

from pathlib import Path
import importlib

from nextcord_ormar.nxalembic.parser import parser

def get_alembic_table_name(app_name):
    return f"alembic.{app_name}"


def get_bot_import():
    nx_alembic = configparser.ConfigParser()
    nx_alembic.read("nxalembic.ini")
    return nx_alembic["nxalembic"]["module"], nx_alembic["nxalembic"]["bot"]


def get_ormar_bot(module_path, module_object) -> Bot:
    bot_module = importlib.import_module(module_path)
    bot = getattr(bot_module, module_object)
    return bot


def get_all_tables(ormar_manager: OrmarManager):
    tables = []
    for app in ormar_manager.apps:
        tables.append(get_alembic_table_name(app))
        tables.extend(ormar_manager.apps[app].metadata.tables.keys())
    return tables


def main():
    args = parser.parse_args()
    if args.tool is None:
        parser.error("too few arguments")
        return

    module_path, module_object = get_bot_import()
    ormar_bot = get_ormar_bot(module_path, module_object)
    all_tables = get_all_tables(ormar_bot._ormar)

    if args.app:
        app_model_meta = ormar_bot._ormar.apps.get(args.app)
        if app_model_meta is None:
            raise Exception(f"App \"{args.app}\" does not exist.")
        apps = [args.app]
    else:
        apps = ormar_bot._ormar.apps.keys()

    bot_path = Path(sys.modules[module_path].__file__)

    for app in apps:
        app_model_meta = ormar_bot._ormar.apps[app]

        metadata_path = Path(sys.modules[app_model_meta._app_module].__file__)

        # If this module is in the same folder as the main bot file, use {module_name}/migrations
        if bot_path.parent == metadata_path.parent:
            version_locations = bot_path.parent / app / "migrations"
        else:
            version_locations = metadata_path.parent / "migrations"

        # version locations need to be a path relative to cwd
        version_locations = version_locations.relative_to(Path(os.getcwd()))
        print("Using migration folder", version_locations)

        # Configuration is dynamically generated from the cog setup
        cfg = Config(ini_section=app)
        # NXAlembic uses a bundled env.py rather than a user one since setup is largely the same for each project
        cfg.set_main_option("script_location", str(Path(__file__).parent / "template"))
        cfg.set_main_option("sqlalchemy.url", ormar_bot._ormar.database_url)
        # This is where this app's migration files will end up
        cfg.set_section_option(app, "version_locations", str(version_locations))
        # This app's alembic migration table
        cfg.set_main_option("version_table", get_alembic_table_name(app))
        # This is used by env.py
        cfg.app_metadata = app_model_meta.metadata
        # Migrations also needs awareness for all tables used by the bot
        cfg.all_tables = all_tables

        match args.tool:
            case "migrate":
                print(f"Migrating {app}...")
                try:
                    command.revision(cfg, "", autogenerate=True)
                except alembic.util.exc.CommandError as e:
                    if e.args[0] == "Target database is not up to date.":
                        print(f"Cannot migrate {app}, a migration hasn't been applied.")
                    else:
                        raise e
            case "upgrade":
                print(f"Upgrading {app}...")
                command.upgrade(cfg, "head", sql=args.sql)
            case "downgrade":
                print(f"Downgrading {app}...")
                command.downgrade(cfg, "-1", sql=args.sql)
    print("Done!")


if __name__ == '__main__':
    main()

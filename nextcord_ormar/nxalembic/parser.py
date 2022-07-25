import argparse

parser = argparse.ArgumentParser(description="Alembic for Nextcord-Ormar")
subparsers = parser.add_subparsers(help="Alembic tool to use", dest="tool")

migrate = subparsers.add_parser("migrate", help="Create a migration for a cog")
migrate.add_argument("--app", help="App to create migration for. Defaults to all apps.")
migrate.add_argument("--empty", help="Create a blank migration file.")
migrate.add_argument("--message", "-m", help="Message to use for the migration.")

upgrade = subparsers.add_parser("upgrade", help="Upgrade a database app")
upgrade.add_argument("--app", help="App to create migration for. Defaults to all apps.")
upgrade.add_argument("--sql", help="Generate SQL for this command instead of executing it.", action="store_true")

downgrade = subparsers.add_parser("downgrade", help="Downgrade a database app")
downgrade.add_argument("app", help="App to create migration for. Defaults to all apps.")
downgrade.add_argument("--sql", help="Generate SQL for this command instead of executing it.", action="store_true")



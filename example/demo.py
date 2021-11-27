import nextcord.ext.commands as commands
import argparse
from nextcord_tortoise import connect_tortoise, attach_argparse_group

# You'll need to use argparse or another argument library to prepare arguments for Aerich
parser = argparse.ArgumentParser(description="Discord Bot")
attach_argparse_group(parser)

# You'll probably want to put these in a configuration file
extensions = ["example_cog"]
token = "Your Discord API Token"
database_uri = "sqlite://db.sqlite3"


bot = commands.Bot(command_prefix="$")


@bot.listen("on_connect")
async def connect_database():  # If you are subclassing bot, put this in your on_connect function
    await connect_tortoise(bot, database_uri)


@bot.listen("on_ready")
async def bot_ready():
    print(f"Logged in as {bot.user}")


if __name__ == '__main__':
    args = parser.parse_args()

    for extension in extensions:
        bot.load_extension(extension)

    # If we have Aerich commands, run Aerich. Else, run the bot.
    if args.aerich:
        from nextcord_tortoise.aerich import run_aerich  # Done to avoid importing Aerich when unused
        run_aerich(bot, args, database_uri)
    else:
        bot.run(token)

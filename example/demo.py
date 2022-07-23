import argparse
from nextcord_ormar import attach_argparse_group
from nextcord_ormar import Bot
from nextcord import Intents
from settings import TORTOISE_CONFIG

intents = Intents.default()
intents.members = True
intents.reactions = True
intents.guilds = True
intents.message_content = True

# You'll need to use argparse or another argument library to prepare arguments for Aerich
parser = argparse.ArgumentParser(description="Discord Bot")
attach_argparse_group(parser)

# You'll probably want to put these in a configuration file
extensions = ["example_cog", "another"]
token = "ODA2NjM5NzI0NTgzMzIxNjUx.YBsXyA.RkOPVZ0kEK50P8W2Z32w_oWUVsc"

bot = Bot(command_prefix="$", database_url="sqlite:///db.sqlite", intents=intents)


@bot.listen("on_ready")
async def bot_ready():
    print(f"Logged in as {bot.user}")


@bot.listen("on_message")
async def bot_message(message):
    print(message)


if __name__ == '__main__':
    args = parser.parse_args()

    for extension in extensions:
        bot.load_extension(extension)

    # If we have Aerich commands, run Aerich. Else, run the bot.
    if args.aerich:
        from nextcord_ormar.aerich import run_aerich  # Done to avoid importing Aerich when unused
        run_aerich(bot, args)
    else:
        bot.run(token)

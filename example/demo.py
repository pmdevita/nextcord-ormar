import argparse
from nextcord_tortoise import attach_argparse_group
from nextcord_tortoise import Bot as TortoiseBot
from settings import TORTOISE_CONFIG

# You'll need to use argparse or another argument library to prepare arguments for Aerich
parser = argparse.ArgumentParser(description="Discord Bot")
attach_argparse_group(parser)

# You'll probably want to put these in a configuration file
extensions = ["example_cog", "another"]
token = "Your Discord API Token"

bot = TortoiseBot(command_prefix="$", tortoise_config=TORTOISE_CONFIG)


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
        run_aerich(bot, args)
    else:
        bot.run(token)

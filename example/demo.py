import os
from nextcord_ormar import Bot
from nextcord import Intents

intents = Intents.default()
intents.members = True
intents.reactions = True
intents.guilds = True
intents.message_content = True


# You'll probably want to put these in a configuration file
extensions = ["example.example_cog", "example.another_cog"]
token = os.environ["TOKEN"]

bot = Bot(command_prefix="$", database_url="sqlite:///db.sqlite", intents=intents)


@bot.listen("on_ready")
async def bot_ready():
    print(f"Logged in as {bot.user}")


for extension in extensions:
    bot.load_extension(extension)

if __name__ == '__main__':
    bot.run(token)

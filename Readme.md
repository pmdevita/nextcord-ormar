# Nextcord-Ormar

[![Documentation Status](https://readthedocs.org/projects/nextcord-ormar/badge/?version=latest&style=for-the-badge)](https://nextcord-ormar.readthedocs.io/en/latest/?badge=latest)

[Formerly Nextcord-Tortoise](docs/goodbye-tortoise.md)

Nextcord-Ormar is a library to help integrate the async Django-inspired ORM
[Ormar](https://github.com/collerek/ormar) with a [Nextcord](https://github.com/nextcord/nextcord/) bot. It's 
designed to compliment the modular cog system of Nextcord. It also comes with NXAlembic, a preconfigured version of
[Alembic](https://github.com/sqlalchemy/alembic) to help with creating and applying database migrations.

Nextcord-Ormar is still in active development, there may be breaking changes as the library is polished up. If you have 
any feedback, feel free to open an issue!

## Quickstart

Install Nextcord-Ormar and Ormar with the correct [database backend](https://collerek.github.io/ormar/install/).

```shell
pip install nextcord-ormar ormar[sqlite]
```


Import Nextcord-Ormar's bot class and pass it your [database URL](https://nextcord-ormar.readthedocs.io/en/latest/connections.html).

```python
from nextcord_ormar import Bot

bot = Bot(command_prefix="$", database_url="sqlite:///db.sqlite")
```

In your cog file, import OrmarApp to create an app, then use AppModel to create a database model. Define your model 
like a [normal Ormar model](https://collerek.github.io/ormar/models/).

If you prefer, you can also define your models elsewhere and import them into your cog.

```python
import ormar
from nextcord_ormar import OrmarApp, AppModel

ModelMeta = OrmarApp.create_app("example")

class ExampleTable(AppModel):
    class Meta(ModelMeta):
        pass
    
    id = ormar.Integer(primary_key=True)
    discord_id = ormar.BigInteger()
    message = ormar.Text()
```

You can then use this model in your cog.

```python
from nextcord.ext import commands

class Example(commands.Cog):
    def __init__(self, nextcord):
        self.nextcord = nextcord

    @commands.command("example")
    async def example(self, ctx: commands.Context, *args):
        new_example = await ExampleTable.objects.create(discord_id=ctx.author.id, message=args[0])
        await ctx.send("Hello!")
```

Before you can start the bot though, you'll need to set up migrations and the database. Create a file called 
`nxalembic.ini` in your project root folder and tell it how to import your bot.

```ini
[nxalembic]
module = example.demo
bot = bot
```

You can think of this as `from module import bot`, or in this instance, `from example.demo import bot`. NXAlembic will 
use it to import your bot along with your definitions for each model.

In the same folder, you can now use the `nxalembic` tool. Create migrations with

```shell
nxalembic migrate
```

Upgrade the database

```shell
nxalembic update
```

Your bot is now ready to start!


### Roadmap

Other than bug fixes as they arise, the current plan is to just add the rest of the Alembic commands to NXAlembic. 
If there is a specific feature you want that is missing from either the bot integration or NXAlembic, feel free to 
open an issue.

### Thanks to

Miguel Grinberg for [Flask-Migrations](https://github.com/miguelgrinberg/Flask-Migrate) which was a useful example.

[Mike Bayer](https://github.com/zzzeek) for [SQLAlchemy](https://www.sqlalchemy.org/) and [Alembic](https://github.com/sqlalchemy/alembic/)



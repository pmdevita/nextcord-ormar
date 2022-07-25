# Nextcord-Ormar

[Formerly Nextcord-Tortoise](docs/goodbye-tortoise.md)

This is a library to help developers integrate the [Ormar database library](https://github.com/collerek/ormar) 
with their Nextcord bot. It's designed to be modular to complement Nextcord's cog system. 
It also provides a wrapper around Alembic called NXAlembic, to help make 
database migrations easy.

This library is currently in alpha, there may be breaking changes as the library is polished up. For now, if you 
would like to install it, run `pip install git+https://github.com/pmdevita/nextcord-ormar`. If you have any feedback, 
don't hesitate to open an issue!


## Quickstart

Import Nextcord-Ormar's bot class and pass it your [database URL](https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls).

```python
from nextcord_ormar import Bot

bot = Bot(command_prefix="$", database_url="sqlite:///db.sqlite")
```

In your cog file, import OrmarApp to create an app, then use AppModel to create a database model. Define your model 
like a [normal Ormar model](https://collerek.github.io/ormar/models/).

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


